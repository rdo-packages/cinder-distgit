%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:             openstack-cinder
Version:          2012.2
Release:          0.5.rc1%{?dist}
Summary:          OpenStack Volume service

Group:            Applications/System
License:          ASL 2.0
URL:              http://www.openstack.org/software/openstack-storage/
Source0:          https://launchpad.net/cinder/folsom/folsom-rc1/+download/cinder-2012.2~rc1.tar.gz
Source1:          cinder.conf
Source2:          cinder.logrotate
Source3:          cinder-tgt.conf

Source10:         openstack-cinder-api.service
Source11:         openstack-cinder-scheduler.service
Source12:         openstack-cinder-volume.service

Source20:         cinder-sudoers

#
# patches_base=folsom-rc1
#
Patch0001: 0001-Ensure-we-don-t-access-the-net-when-building-docs.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-sphinx
BuildRequires:    python-setuptools
BuildRequires:    python-netaddr
BuildRequires:    openstack-utils

Requires:         openstack-utils
Requires:         python-cinder = %{version}-%{release}

# as convenience
Requires:         python-cinderclient

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(pre):    shadow-utils

Requires:         lvm2
Requires:         scsi-target-utils

%description
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.


%package -n       python-cinder
Summary:          OpenStack Volume Python libraries
Group:            Applications/System

Requires:         sudo

Requires:         MySQL-python

Requires:         python-paramiko

Requires:         python-qpid
Requires:         python-kombu
Requires:         python-amqplib

Requires:         python-daemon
Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-netaddr
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-cheetah

Requires:         python-sqlalchemy
Requires:         python-migrate

Requires:         python-paste-deploy
Requires:         python-routes
Requires:         python-webob

Requires:         python-glanceclient >= 1:0

%description -n   python-cinder
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.

This package contains the cinder Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Volume
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    systemd-units
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
%setup -q -n cinder-%{version}

%patch0001 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete

find cinder -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

%build

# Move authtoken configuration out of paste.ini
openstack-config --del etc/cinder/api-paste.ini filter:authtoken admin_tenant_name
openstack-config --del etc/cinder/api-paste.ini filter:authtoken admin_user
openstack-config --del etc/cinder/api-paste.ini filter:authtoken admin_password
openstack-config --del etc/cinder/api-paste.ini filter:authtoken auth_host
openstack-config --del etc/cinder/api-paste.ini filter:authtoken auth_port
openstack-config --del etc/cinder/api-paste.ini filter:authtoken auth_protocol

%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

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
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/cinder/cinder.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder/volumes
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/tgt/conf.d/cinder.conf
install -p -D -m 640 etc/cinder/rootwrap.conf %{buildroot}%{_sysconfdir}/cinder/rootwrap.conf
install -p -D -m 640 etc/cinder/api-paste.ini %{buildroot}%{_sysconfdir}/cinder/api-paste.ini
install -p -D -m 640 etc/cinder/policy.json %{buildroot}%{_sysconfdir}/cinder/policy.json

# Install initscripts for services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/openstack-cinder-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/openstack-cinder-scheduler.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/openstack-cinder-volume.service

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
#TODO:reserve 165 in the setup package
getent group cinder >/dev/null || groupadd -r cinder --gid 165
if ! getent passwd cinder >/dev/null; then
  useradd -u 165 -r -g cinder -G cinder,nobody -d %{_sharedstatedir}/cinder -s /sbin/nologin -c "OpenStack Cinder Daemons" cinder
fi
exit 0

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    for svc in volume api scheduler; do
        /bin/systemctl --no-reload disable openstack-cinder-${svc}.service > /dev/null 2>&1 || :
        /bin/systemctl stop openstack-cinder-${svc}.service > /dev/null 2>&1 || :
    done
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in volume api scheduler; do
        /bin/systemctl try-restart openstack-cinder-${svc}.service >/dev/null 2>&1 || :
    done
fi

%files
%doc LICENSE

%dir %{_sysconfdir}/cinder
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/cinder.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/api-paste.ini
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/rootwrap.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-cinder
%config(noreplace) %{_sysconfdir}/sudoers.d/cinder
%config(noreplace) %{_sysconfdir}/tgt/conf.d/cinder.conf

%dir %attr(0755, cinder, root) %{_localstatedir}/log/cinder
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
%doc LICENSE
%{python_sitelib}/cinder
%{python_sitelib}/cinder-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
* Fri Sep 21 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.5.rc1
- Update to Folsom RC1

* Fri Sep 21 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.4.f3
- Fix to ensure that tgt configuration is honored

* Mon Sep 17 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.3.f3
- Move user config out of /etc/cinder/api-paste.ini
- Require python-cinderclient

* Mon Sep  3 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.2.f3
- Initial release
