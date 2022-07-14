# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# Temporary disable doc until https://bugs.launchpad.net/tripleo/+bug/1838225 is fixed
%global with_doc %{!?_without_doc:0}%{?_without_doc:1}
%global service cinder

# guard for Red Hat OpenStack Platform supported cinder
%global rhosp 0
%global common_desc \
OpenStack Volume (codename Cinder) provides services to manage and \
access block storage volumes for use by Virtual Machine instances.

Name:             openstack-%{service}
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          15.6.0
Release:          1%{?dist}
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
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-reno
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-netaddr
BuildRequires:    systemd
BuildRequires:    git
BuildRequires:    python%{pyver}-os-brick
BuildRequires:    python%{pyver}-pyparsing
BuildRequires:    python%{pyver}-pytz
BuildRequires:    openstack-macros
# Required to build cinder.conf
BuildRequires:    python%{pyver}-cursive
BuildRequires:    python%{pyver}-google-api-client >= 1.4.2
BuildRequires:    python%{pyver}-keystonemiddleware
BuildRequires:    python%{pyver}-glanceclient >= 1:2.15.0
BuildRequires:    python%{pyver}-novaclient >= 9.1.0
BuildRequires:    python%{pyver}-swiftclient >= 3.2.0
BuildRequires:    python%{pyver}-oslo-db
BuildRequires:    python%{pyver}-oslo-config >= 2:5.2.0
BuildRequires:    python%{pyver}-oslo-policy
BuildRequires:    python%{pyver}-oslo-privsep
BuildRequires:    python%{pyver}-oslo-reports
BuildRequires:    python%{pyver}-oslotest
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-oslo-versionedobjects
BuildRequires:    python%{pyver}-oslo-vmware
BuildRequires:    python%{pyver}-os-win
BuildRequires:    python%{pyver}-castellan
BuildRequires:    python%{pyver}-cryptography
BuildRequires:    python%{pyver}-osprofiler
BuildRequires:    python%{pyver}-paramiko
BuildRequires:    python%{pyver}-suds
BuildRequires:    python%{pyver}-taskflow
BuildRequires:    python%{pyver}-tooz
BuildRequires:    python%{pyver}-oslo-log
BuildRequires:    python%{pyver}-oslo-i18n
BuildRequires:    python%{pyver}-barbicanclient
BuildRequires:    python%{pyver}-requests
BuildRequires:    python%{pyver}-defusedxml

# Required to compile translation files
BuildRequires:    python%{pyver}-babel

# Needed for unit tests
BuildRequires:    python%{pyver}-ddt
BuildRequires:    python%{pyver}-fixtures
BuildRequires:    python%{pyver}-mock
BuildRequires:    python%{pyver}-oslotest
BuildRequires:    python%{pyver}-subunit
BuildRequires:    python%{pyver}-testtools
BuildRequires:    python%{pyver}-testrepository
BuildRequires:    python%{pyver}-testresources
BuildRequires:    python%{pyver}-testscenarios
BuildRequires:    python%{pyver}-os-testr

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-decorator
BuildRequires:    python-lxml
BuildRequires:    python-retrying
BuildRequires:    python-rtslib
%else
BuildRequires:    python%{pyver}-decorator
BuildRequires:    python%{pyver}-lxml
BuildRequires:    python%{pyver}-retrying
BuildRequires:    python%{pyver}-rtslib
%endif


Requires:         python%{pyver}-%{service} = %{epoch}:%{version}-%{release}

# we dropped the patch to remove PBR for Delorean
Requires:         python%{pyver}-pbr

# as convenience
Requires:         python%{pyver}-cinderclient

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
Requires(pre):    shadow-utils

Requires:         lvm2
Requires:         python%{pyver}-osprofiler

# Handle python2 exception
%if %{pyver} == 2
Requires:         python-rtslib
Requires:         python-pyudev
# required for cinder-manage
Requires:         python-prettytable >= 0.7.1
%else
Requires:         python%{pyver}-rtslib
Requires:         python%{pyver}-pyudev
# required for cinder-manage
Requires:         python%{pyver}-prettytable >= 0.7.1
%endif


%description
%{common_desc}


%package -n       python%{pyver}-%{service}
Summary:          OpenStack Volume Python libraries
%{?python_provide:%python_provide python%{pyver}-%{service}}
Group:            Applications/System

Requires:         sudo

Requires:         cryptsetup
Requires:         cracklib-dicts
Requires:         qemu-img >= 2.10.0
Requires:         sysfsutils
Requires:         python%{pyver}-paramiko >= 2.0.0
Requires:         python%{pyver}-simplejson >= 3.5.1
Requires:         python%{pyver}-jsonschema >= 2.6.0

Requires:         python%{pyver}-castellan >= 0.16.0
Requires:         python%{pyver}-cursive >= 0.2.1
Requires:         python%{pyver}-etcd3gw
Requires:         python%{pyver}-eventlet >= 0.22.0
Requires:         python%{pyver}-greenlet >= 0.4.10
Requires:         python%{pyver}-iso8601 >= 0.1.11
Requires:         python%{pyver}-stevedore >= 1.20.0
Requires:         python%{pyver}-suds
Requires:         python%{pyver}-tooz >= 1.58.0

Requires:         python%{pyver}-sqlalchemy >= 1.0.10
Requires:         python%{pyver}-routes >= 2.3.1
Requires:         python%{pyver}-webob >= 1.7.1

Requires:         python%{pyver}-barbicanclient >= 4.5.2
Requires:         python%{pyver}-glanceclient >= 1:2.15.0
Requires:         python%{pyver}-keystoneclient >= 1:3.15.0
Requires:         python%{pyver}-novaclient >= 9.1.0
Requires:         python%{pyver}-swiftclient >= 3.2.0

Requires:         python%{pyver}-six >= 1.10.0
Requires:         python%{pyver}-psutil >= 3.2.2

Requires:         python%{pyver}-google-api-client >= 1.4.2

Requires:         python%{pyver}-keystonemiddleware >= 4.21.0
Requires:         python%{pyver}-keystoneauth1 >= 3.7.0
Requires:         python%{pyver}-osprofiler >= 1.4.0
Requires:         python%{pyver}-os-brick >= 2.8.0
Requires:         python%{pyver}-os-win >= 3.0.0
Requires:         python%{pyver}-oslo-config >= 2:5.2.0
Requires:         python%{pyver}-oslo-concurrency >= 3.26.0
Requires:         python%{pyver}-oslo-context >= 2.19.2
Requires:         python%{pyver}-oslo-db >= 4.27.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-log >= 3.36.0
Requires:         python%{pyver}-oslo-middleware >= 3.31.0
Requires:         python%{pyver}-oslo-messaging >= 6.4.0
Requires:         python%{pyver}-oslo-policy >= 1.44.1
Requires:         python%{pyver}-oslo-privsep >= 1.32.0
Requires:         python%{pyver}-oslo-reports >= 1.18.0
Requires:         python%{pyver}-oslo-rootwrap >= 5.8.0
Requires:         python%{pyver}-oslo-serialization >= 2.18.0
Requires:         python%{pyver}-oslo-service >= 1.24.0
Requires:         python%{pyver}-oslo-upgradecheck >= 0.1.0
Requires:         python%{pyver}-oslo-utils >= 3.34.0
Requires:         python%{pyver}-oslo-versionedobjects >= 1.31.2
Requires:         python%{pyver}-oslo-vmware >= 2.17.0
Requires:         python%{pyver}-taskflow >= 3.2.0

Requires:         iscsi-initiator-utils

Requires:         python%{pyver}-oauth2client >= 1.5.0
Requires:         python%{pyver}-requests >= 2.14.2
Requires:         python%{pyver}-pyparsing >= 2.1.0
Requires:         python%{pyver}-pytz

Requires:         python%{pyver}-cryptography >= 2.1

Requires:         python%{pyver}-defusedxml >= 0.5.0

# Handle python2 exception
%if %{pyver} == 2
Requires:         python-lxml >= 3.2.1
Requires:         python-migrate >= 0.11.0
Requires:         python-paste
Requires:         python-paste-deploy
Requires:         python-httplib2 >= 0.9.1
Requires:         python-retrying >= 1.2.3
Requires:         python-decorator
Requires:         python-enum34
Requires:         python-ipaddress
%else
Requires:         python%{pyver}-lxml >= 3.2.1
Requires:         python%{pyver}-migrate >= 0.11.0
Requires:         python%{pyver}-paste
Requires:         python%{pyver}-paste-deploy
Requires:         python%{pyver}-httplib2 >= 0.9.1
Requires:         python%{pyver}-retrying >= 1.2.3
Requires:         python%{pyver}-decorator
%endif

%if 0%{?rhosp} == 1
# Required by DataCore driver
Requires:         python3-websocket-client
%endif

# Required by the volume_copy_bps_limit option
# at least where the package is available
%if 0%{?rhel} && 0%{?rhel} < 9
Requires:         libcgroup-tools
%endif


%description -n   python%{pyver}-%{service}
%{common_desc}

This package contains the %{service} Python library.

%package -n python%{pyver}-%{service}-tests
Summary:        Cinder tests
%{?python_provide:%python_provide python%{pyver}-%{service}-tests}
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

# Added test requirements
Requires:       python%{pyver}-hacking
Requires:       python%{pyver}-ddt
Requires:       python%{pyver}-fixtures
Requires:       python%{pyver}-mock
Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-subunit
Requires:       python%{pyver}-testtools
Requires:       python%{pyver}-testrepository
Requires:       python%{pyver}-testresources
Requires:       python%{pyver}-testscenarios
Requires:       python%{pyver}-stestr


%description -n python%{pyver}-%{service}-tests
%{common_desc}

This package contains the Cinder test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Volume
Group:            Documentation

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    graphviz

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-sphinxcontrib-apidoc
BuildRequires:    python%{pyver}-sphinx-feature-classification
# Required to build module documents
BuildRequires:    python%{pyver}-eventlet
BuildRequires:    python%{pyver}-routes
BuildRequires:    python%{pyver}-sqlalchemy
BuildRequires:    python%{pyver}-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python%{pyver}-iso8601 >= 0.1.9

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-migrate
%else
BuildRequires:    python%{pyver}-migrate
%endif


%description      doc
%{common_desc}

This package contains documentation files for %{service}.
%endif

%prep
%autosetup -n %{service}-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +
sed -i 's/\/usr\/bin\/env python/\/usr\/bin\/env python%{pyver}/' tools/generate_driver_list.py

sed -i 's/%{version}.%{milestone}/%{version}/' PKG-INFO

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
# Generate config file
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=tools/config/%{service}-config-generator.conf

# Build
%{pyver_build}

# Generate i18n files
# (amoralej) we can remove '-D cinder' once https://review.openstack.org/#/c/439501/ is merged
%{pyver_bin} setup.py compile_catalog -d build/lib/%{service}/locale -D cinder

%install
%{pyver_install}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

%if 0%{?with_doc}
# FIXME(ykarel) Temporary disable warning as error until https://review.openstack.org/#/c/558263/ merges.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
# FIXME(ykarel) Temporary disable warning as error until https://review.openstack.org/#/c/558263/ merges.
sphinx-build-%{pyver} -b man doc/source doc/build/man
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
install -p -D -m 640 etc/%{service}/resource_filters.json %{buildroot}%{_sysconfdir}/%{service}/resource_filters.json
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
rm -f %{buildroot}%{pyver_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{pyver_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{pyver_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

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
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/resource_filters.json
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

%files -n python%{pyver}-%{service} -f %{service}.lang
%{?!_licensedir: %global license %%doc}
%license LICENSE
%{pyver_sitelib}/%{service}
%{pyver_sitelib}/%{service}-*.egg-info
%exclude %{pyver_sitelib}/%{service}/test.py
%exclude %{pyver_sitelib}/%{service}/tests

%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{service}/test.py
%{pyver_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
* Wed May 12 2021 RDO <dev@lists.rdoproject.org> 1:15.6.0-1
- Update to 15.6.0

* Thu Apr 08 2021 RDO <dev@lists.rdoproject.org> 1:15.5.0-1
- Update to 15.5.0

* Wed Dec 09 2020 RDO <dev@lists.rdoproject.org> 1:15.4.1-1
- Update to 15.4.1

* Wed Sep 30 2020 RDO <dev@lists.rdoproject.org> 1:15.4.0-1
- Update to 15.4.0

* Wed Jun 24 2020 RDO <dev@lists.rdoproject.org> 1:15.3.0-1
- Update to 15.3.0

* Fri Jun 05 2020 RDO <dev@lists.rdoproject.org> 1:15.2.0-1
- Update to 15.2.0

* Tue Apr 07 2020 Luigi Toscano <ltoscano@redhat.com> 1:15.1.0-2
- Add cryptsetup dependencies

* Fri Apr 03 2020 RDO <dev@lists.rdoproject.org> 1:15.1.0-1
- Update to 15.1.0

* Mon Jan 06 2020 RDO <dev@lists.rdoproject.org> 1:15.0.1-1
- Update to 15.0.1

* Mon Nov 18 2019 Eric Harney <eharney@redhat.com> 1:15.0.0-2
- Remove runtime dep on babel

* Wed Oct 16 2019 RDO <dev@lists.rdoproject.org> 1:15.0.0-1
- Update to 15.0.0

* Mon Oct 07 2019 RDO <dev@lists.rdoproject.org> 1:15.0.0-0.2.0rc1
- Update to 15.0.0.0rc2

* Mon Sep 30 2019 RDO <dev@lists.rdoproject.org> 1:15.0.0-0.1.0rc1
- Update to 15.0.0.0rc1


