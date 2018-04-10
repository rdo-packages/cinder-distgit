%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# FIXME(ykarel) disable doc build until sphinxcontrib-apidoc package is
# available in RDO https://bugzilla.redhat.com/show_bug.cgi?id=1565504
%global with_doc %{!?_without_doc:0}%{?_without_doc:1}
%global service cinder

%global common_desc \
OpenStack Volume (codename Cinder) provides services to manage and \
access block storage volumes for use by Virtual Machine instances.

Name:             openstack-%{service}
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          XXX
Release:          XXX
Summary:          OpenStack Volume service

License:          ASL 2.0
URL:              http://www.openstack.org/software/openstack-storage/
Source0:          https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

Source1:          %{service}-dist.conf
Source2:          %{service}.logrotate

Source10:         openstack-%{service}-api.service
Source11:         openstack-%{service}-scheduler.service
Source12:         openstack-%{service}-volume.service
Source13:         openstack-%{service}-backup.service
Source20:         %{service}-sudoers


BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-d2to1
BuildRequires:    python2-openstackdocstheme
BuildRequires:    python2-pbr
BuildRequires:    python2-reno
BuildRequires:    python2-sphinx
BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python2-netaddr
BuildRequires:    systemd
BuildRequires:    git
BuildRequires:    openstack-macros
BuildRequires:    os-brick
BuildRequires:    python2-pyparsing
BuildRequires:    python2-pytz
BuildRequires:    python-decorator
BuildRequires:    openstack-macros
# Required to build cinder.conf
BuildRequires:    python2-google-api-client >= 1.4.2
BuildRequires:    python2-keystonemiddleware
BuildRequires:    python2-glanceclient >= 2.8.0
BuildRequires:    python2-novaclient >= 9.1.0
BuildRequires:    python2-swiftclient >= 3.2.0
BuildRequires:    python2-oslo-db
BuildRequires:    python2-oslo-config >= 2:5.1.0
BuildRequires:    python2-oslo-policy
BuildRequires:    python2-oslo-reports
BuildRequires:    python2-oslotest
BuildRequires:    python2-oslo-utils
BuildRequires:    python2-oslo-versionedobjects
BuildRequires:    python2-oslo-vmware
BuildRequires:    python2-os-win
BuildRequires:    python2-castellan
BuildRequires:    python2-cryptography
BuildRequires:    python-lxml
BuildRequires:    python2-osprofiler
BuildRequires:    python2-paramiko
BuildRequires:    python2-suds
BuildRequires:    python2-taskflow
BuildRequires:    python2-tooz
BuildRequires:    python2-oslo-log
BuildRequires:    python2-oslo-i18n
BuildRequires:    python2-barbicanclient
BuildRequires:    python2-requests
BuildRequires:    python-retrying
BuildRequires:    python2-defusedxml

# Required to compile translation files
BuildRequires:    python2-babel

# Needed for unit tests
BuildRequires:    python2-ddt
BuildRequires:    python2-fixtures
BuildRequires:    python2-mock
BuildRequires:    python2-oslotest
BuildRequires:    python2-subunit
BuildRequires:    python2-testtools
BuildRequires:    python2-testrepository
BuildRequires:    python2-testresources
BuildRequires:    python2-testscenarios
BuildRequires:    python2-os-testr
BuildRequires:    python-rtslib

Requires:         python-%{service} = %{epoch}:%{version}-%{release}

# we dropped the patch to remove PBR for Delorean
Requires:         python2-pbr

# as convenience
Requires:         python2-cinderclient

%{?systemd_requires}
Requires(pre):    shadow-utils

Requires:         lvm2
Requires:         python2-osprofiler
Requires:         python-rtslib
Requires:         python-pyudev

# required for cinder-manage
Requires:         python-prettytable >= 0.7.1

%description
%{common_desc}


%package -n       python-%{service}
Summary:          OpenStack Volume Python libraries
Group:            Applications/System

Requires:         sudo

Requires:         qemu-img
Requires:         sysfsutils
Requires:         os-brick >= 2.1.1
Requires:         python2-paramiko >= 2.0
Requires:         python-simplejson >= 3.5.1
Requires:         python2-jsonschema >= 2.6.0
Requires:         python2-os-win >= 3.0.0
Requires:         python2-oslo-vmware >= 2.17.0

Requires:         python2-castellan >= 0.16.0
Requires:         python2-eventlet >= 0.18.2
Requires:         python2-greenlet >= 0.4.10
Requires:         python2-iso8601 >= 0.1.11
Requires:         python-lxml >= 3.2.1
Requires:         python2-stevedore >= 1.20.0
Requires:         python2-suds
Requires:         python2-tooz >= 1.58.0

Requires:         python2-sqlalchemy >= 1.0.10
Requires:         python-migrate >= 0.11.0

Requires:         python-paste
Requires:         python-paste-deploy
Requires:         python2-routes >= 2.3.1
Requires:         python-webob >= 1.7.1

Requires:         python2-glanceclient >= 1:2.8.0
Requires:         python2-swiftclient >= 3.2.0
Requires:         python2-keystoneclient >= 1:3.8.0
Requires:         python2-novaclient >= 9.1.0

Requires:         python2-oslo-config >= 2:5.1.0
Requires:         python2-six >= 1.10.0
Requires:         python2-psutil >= 3.2.2

Requires:         python2-babel
Requires:         python2-google-api-client >= 1.4.2

Requires:         python2-oslo-rootwrap >= 5.8.0
Requires:         python2-oslo-utils >= 3.33.0
Requires:         python2-oslo-serialization >= 2.18.0
Requires:         python2-oslo-db >= 4.27.0
Requires:         python2-oslo-context >= 2.19.2
Requires:         python2-oslo-concurrency >= 3.25.0
Requires:         python2-oslo-middleware >= 3.31.0
Requires:         python2-taskflow >= 2.16.0
Requires:         python2-oslo-messaging >= 5.29.0
Requires:         python2-oslo-policy >= 1.30.0
Requires:         python2-oslo-reports >= 1.18.0
Requires:         python2-oslo-service >= 1.24.0
Requires:         python2-oslo-versionedobjects >= 1.31.2

Requires:         iscsi-initiator-utils

Requires:         python2-osprofiler >= 1.4.0

Requires:         python-httplib2 >= 0.9.1
Requires:         python2-oauth2client >= 1.5.0

Requires:         python2-oslo-log >= 3.36.0
Requires:         python2-oslo-i18n >= 3.15.3
Requires:         python2-barbicanclient >= 4.0.0
Requires:         python2-requests >= 2.14.2
Requires:         python-retrying >= 1.2.3
Requires:         python2-pyparsing >= 2.1.0
Requires:         python2-pytz
Requires:         python-decorator
Requires:         python-enum34
Requires:         python-ipaddress

Requires:         python2-keystonemiddleware >= 4.17.0
Requires:         python2-keystoneauth1 >= 3.3.0

Requires:         python2-oslo-privsep >= 1.23.0

Requires:         python2-cryptography >= 1.7.2

Requires:         python2-defusedxml >= 0.5.0

%description -n   python-%{service}
%{common_desc}

This package contains the %{service} Python library.

%package -n python-%{service}-tests
Summary:        Cinder tests
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

# Added test requirements
Requires:       python2-hacking
Requires:       python-anyjson
Requires:       python2-ddt
Requires:       python2-fixtures
Requires:       python2-mock
Requires:       python2-mox3
Requires:       python2-oslotest
Requires:       python2-subunit
Requires:       python2-testtools
Requires:       python2-testrepository
Requires:       python2-testresources
Requires:       python2-testscenarios
Requires:       python2-os-testr

%description -n python-%{service}-tests
%{common_desc}

This package contains the Cinder test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Volume
Group:            Documentation

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python2-eventlet
BuildRequires:    python2-routes
BuildRequires:    python2-sqlalchemy
BuildRequires:    python-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate
BuildRequires:    python2-iso8601 >= 0.1.9

%description      doc
%{common_desc}

This package contains documentation files for %{service}.
%endif

%prep
%autosetup -n %{service}-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i 's/%{version}.%{milestone}/%{version}/' PKG-INFO

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=tools/config/%{service}-config-generator.conf

# Build
%{__python2} setup.py build

# Generate i18n files
# (amoralej) we can remove '-D cinder' once https://review.openstack.org/#/c/439501/ is merged
%{__python2} setup.py compile_catalog -d build/lib/%{service}/locale -D cinder

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

%if 0%{?with_doc}
# FIXME(ykarel) Temporary disable warning as error until https://review.openstack.org/#/c/558263/ merges.
sphinx-build -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
# FIXME(ykarel) Temporary disable warning as error until https://review.openstack.org/#/c/558263/ merges.
sphinx-build -b man doc/source doc/build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif


# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}/volumes
install -p -D -m 640 etc/%{service}/rootwrap.conf %{buildroot}%{_sysconfdir}/%{service}/rootwrap.conf
install -p -D -m 640 etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini
install -p -D -m 640 etc/%{service}/%{service}.conf.sample %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf

# Install initscripts for services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/openstack-%{service}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/openstack-%{service}-scheduler.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/openstack-%{service}-volume.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/openstack-%{service}-backup.service

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/%{service}

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{service}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{service}

# Install rootwrap files in /usr/share/cinder/rootwrap
mkdir -p %{buildroot}%{_datarootdir}/%{service}/rootwrap/
install -p -D -m 644 etc/%{service}/rootwrap.d/* %{buildroot}%{_datarootdir}/%{service}/rootwrap/


# Symlinks to rootwrap config files
mkdir -p %{buildroot}%{_sysconfdir}/%{service}/rootwrap.d
for filter in %{_datarootdir}/os-brick/rootwrap/*.filters; do
ln -s $filter %{buildroot}%{_sysconfdir}/%{service}/rootwrap.d/
done

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

# Remove unneeded in production stuff
rm -f %{buildroot}/usr/share/doc/%{service}/README*

# Remove duplicate config files under /usr/etc/
rm -rf %{buildroot}%{_prefix}/etc

# FIXME(jpena): unit tests are taking too long in the current DLRN infra
# Until we have a better architecture, let's not run them when under DLRN
%if 0%{!?dlrn}
%check
OS_TEST_PATH=./%{service}/tests/unit ostestr --concurrency=2
%endif

%pre
getent group %{service} >/dev/null || groupadd -r %{service} --gid 165
if ! getent passwd %{service} >/dev/null; then
  useradd -u 165 -r -g %{service} -G %{service},nobody -d %{_sharedstatedir}/%{service} -s /sbin/nologin -c "OpenStack Cinder Daemons" %{service}
fi
exit 0

%post
%systemd_post openstack-%{service}-volume
%systemd_post openstack-%{service}-api
%systemd_post openstack-%{service}-scheduler
%systemd_post openstack-%{service}-backup

%preun
%systemd_preun openstack-%{service}-volume
%systemd_preun openstack-%{service}-api
%systemd_preun openstack-%{service}-scheduler
%systemd_preun openstack-%{service}-backup

%postun
%systemd_postun_with_restart openstack-%{service}-volume
%systemd_postun_with_restart openstack-%{service}-api
%systemd_postun_with_restart openstack-%{service}-scheduler
%systemd_postun_with_restart openstack-%{service}-backup

%files
%dir %{_sysconfdir}/%{service}
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/rootwrap.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{service}
%config(noreplace) %{_sysconfdir}/sudoers.d/%{service}
%{_sysconfdir}/%{service}/rootwrap.d/
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf

%dir %attr(0750, %{service}, root) %{_localstatedir}/log/%{service}
%dir %attr(0755, %{service}, root) %{_localstatedir}/run/%{service}
%dir %attr(0755, %{service}, root) %{_sysconfdir}/%{service}/volumes

%{_bindir}/%{service}-*
%{_unitdir}/*.service
%{_datarootdir}/%{service}
%if 0%{?with_doc}
%{_mandir}/man1/%{service}*.1.gz
%endif

%defattr(-, %{service}, %{service}, -)
%dir %{_sharedstatedir}/%{service}
%dir %{_sharedstatedir}/%{service}/tmp

%files -n python-%{service} -f %{service}.lang
%{?!_licensedir: %global license %%doc}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/test.py
%exclude %{python2_sitelib}/%{service}/tests

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/test.py
%{python2_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
