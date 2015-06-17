%global release_name kilo
%global service cinder

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:             openstack-cinder
Version:          2015.1.0
Release:          3%{?milestone}%{?dist}
Summary:          OpenStack Volume service

License:          ASL 2.0
URL:              http://www.openstack.org/software/openstack-storage/
Source0:          http://launchpad.net/%{service}/%{release_name}/%{version}/+download/%{service}-%{upstream_version}.tar.gz

Source1:          cinder-dist.conf
Source2:          cinder.logrotate
Source3:          cinder.conf.sample

Source10:         openstack-cinder-api.service
Source11:         openstack-cinder-scheduler.service
Source12:         openstack-cinder-volume.service
Source13:         openstack-cinder-backup.service
Source20:         cinder-sudoers

Patch0001: 0001-Disallow-backing-files-when-uploading-volumes-to-ima.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-d2to1
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-pbr
BuildRequires:    python-sphinx
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-netaddr
BuildRequires:    systemd
BuildRequires:    git

Requires:         openstack-utils
Requires:         python-cinder = %{version}-%{release}

# we dropped the patch to remove PBR for Delorean
Requires:         python-pbr

# as convenience
Requires:         python-cinderclient

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils

Requires:         lvm2
Requires:         python-osprofiler
Requires:         python-rtslib

%description
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.


%package -n       python-cinder
Summary:          OpenStack Volume Python libraries
Group:            Applications/System

Requires:         sudo

Requires:         MySQL-python

Requires:         qemu-img
Requires:         sysfsutils

Requires:         python-paramiko

Requires:         python-qpid
Requires:         python-kombu
Requires:         python-amqplib

Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-netaddr
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-cheetah
Requires:         python-stevedore
Requires:         python-suds

Requires:         python-sqlalchemy
Requires:         python-migrate

Requires:         python-paste-deploy
Requires:         python-routes
Requires:         python-webob

Requires:         python-glanceclient >= 1:0
Requires:         python-swiftclient >= 1.2
Requires:         python-keystoneclient
Requires:         python-novaclient >= 1:2.15

Requires:         python-oslo-config >= 1:1.2.0
Requires:         python-oslo-db >= 1.0.0
Requires:         python-six >= 1.5.0

Requires:         python-babel
Requires:         python-lockfile

Requires:         python-oslo-rootwrap
Requires:         python-oslo-utils
Requires:         python-oslo-serialization
Requires:         python-oslo-db
Requires:         python-oslo-context
Requires:         python-oslo-concurrency
Requires:         python-oslo-middleware
Requires:         python-taskflow >= 0.7.1
Requires:         python-oslo-messaging >= 1.8.0
Requires:         python-keystonemiddleware >= 1.5.0

Requires:         libcgroup-tools
Requires:         iscsi-initiator-utils

Requires:         python-osprofiler

%description -n   python-cinder
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.

This package contains the cinder Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Volume
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-eventlet
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate, python-iso8601

%description      doc
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.

This package contains documentation files for cinder.
%endif

%prep
%autosetup -n cinder-%{upstream_version} -S git

cp %{SOURCE3} etc/cinder/cinder.conf.sample

find . \( -name .gitignore -o -name .placeholder \) -delete

find cinder -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

pushd doc

%if 0%{?with_doc}
SPHINX_DEBUG=1 sphinx-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo
%endif

# Create dir link to avoid a sphinx-build exception
mkdir -p build/man/.doctrees/
ln -s .  build/man/.doctrees/man
SPHINX_DEBUG=1 sphinx-build -b man -c source source/man build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/

popd

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/cinder
install -d -m 755 %{buildroot}%{_sharedstatedir}/cinder/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/cinder

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/cinder/cinder-dist.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder/volumes
install -p -D -m 640 etc/cinder/rootwrap.conf %{buildroot}%{_sysconfdir}/cinder/rootwrap.conf
install -p -D -m 640 etc/cinder/api-paste.ini %{buildroot}%{_sysconfdir}/cinder/api-paste.ini
install -p -D -m 640 etc/cinder/policy.json %{buildroot}%{_sysconfdir}/cinder/policy.json
install -p -D -m 640 etc/cinder/cinder.conf.sample %{buildroot}%{_sysconfdir}/cinder/cinder.conf

# Install initscripts for services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/openstack-cinder-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/openstack-cinder-scheduler.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/openstack-cinder-volume.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/openstack-cinder-backup.service

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/cinder

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-cinder

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/cinder

# Install rootwrap files in /usr/share/cinder/rootwrap
mkdir -p %{buildroot}%{_datarootdir}/cinder/rootwrap/
install -p -D -m 644 etc/cinder/rootwrap.d/* %{buildroot}%{_datarootdir}/cinder/rootwrap/

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/cinder-debug
rm -fr %{buildroot}%{python_sitelib}/cinder/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/cinder/README*

%pre
getent group cinder >/dev/null || groupadd -r cinder --gid 165
if ! getent passwd cinder >/dev/null; then
  useradd -u 165 -r -g cinder -G cinder,nobody -d %{_sharedstatedir}/cinder -s /sbin/nologin -c "OpenStack Cinder Daemons" cinder
fi
exit 0

%post
%systemd_post openstack-cinder-volume
%systemd_post openstack-cinder-api
%systemd_post openstack-cinder-scheduler
%systemd_post openstack-cinder-backup

%preun
%systemd_preun openstack-cinder-volume
%systemd_preun openstack-cinder-api
%systemd_preun openstack-cinder-scheduler
%systemd_preun openstack-cinder-backup

%postun
%systemd_postun_with_restart openstack-cinder-volume
%systemd_postun_with_restart openstack-cinder-api
%systemd_postun_with_restart openstack-cinder-scheduler
%systemd_postun_with_restart openstack-cinder-backup

%files
%dir %{_sysconfdir}/cinder
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/cinder.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/api-paste.ini
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/rootwrap.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-cinder
%config(noreplace) %{_sysconfdir}/sudoers.d/cinder
%attr(-, root, cinder) %{_datadir}/cinder/cinder-dist.conf

%dir %attr(0750, cinder, root) %{_localstatedir}/log/cinder
%dir %attr(0755, cinder, root) %{_localstatedir}/run/cinder
%dir %attr(0755, cinder, root) %{_sysconfdir}/cinder/volumes

%{_bindir}/cinder-*
%{_unitdir}/*.service
%{_datarootdir}/cinder
%{_mandir}/man1/cinder*.1.gz

%defattr(-, cinder, cinder, -)
%dir %{_sharedstatedir}/cinder
%dir %{_sharedstatedir}/cinder/tmp

%files -n python-cinder
%{?!_licensedir: %global license %%doc}
%license LICENSE
%{python2_sitelib}/cinder
%{python2_sitelib}/cinder-*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
* Wed Jun 17 2015 Haïkel Guémar <hguemar@fedoraproject.org> 2015.1.0-3
- Fix CVE-2015-1851 (RHBZ #1231822)

* Mon May 04 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-2
- update keystone_authtoken section in sample conf

* Thu Apr 30 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-1
- OpenStack Kilo release
