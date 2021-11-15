%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# Temporary disable doc until https://bugs.launchpad.net/tripleo/+bug/1838225 is fixed
%global with_doc %{!?_without_doc:0}%{?_without_doc:1}
%global service cinder

%global common_desc \
OpenStack Volume (codename Cinder) provides services to manage and \
access block storage volumes for use by Virtual Machine instances.

Name:             openstack-%{service}
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          16.4.2
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
BuildRequires:    python3-pbr
BuildRequires:    python3-reno
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-netaddr
BuildRequires:    systemd
BuildRequires:    git-core
BuildRequires:    python3-os-brick
BuildRequires:    python3-pyparsing
BuildRequires:    python3-pytz
BuildRequires:    openstack-macros
# Required to build cinder.conf
BuildRequires:    python3-cursive
BuildRequires:    python3-google-api-client >= 1.4.2
BuildRequires:    python3-keystonemiddleware
BuildRequires:    python3-glanceclient >= 1:2.15.0
BuildRequires:    python3-novaclient >= 9.1.0
BuildRequires:    python3-swiftclient >= 3.2.0
BuildRequires:    python3-oslo-db
BuildRequires:    python3-oslo-config >= 2:5.2.0
BuildRequires:    python3-oslo-policy
BuildRequires:    python3-oslo-privsep
BuildRequires:    python3-oslo-reports
BuildRequires:    python3-oslotest
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-oslo-versionedobjects
BuildRequires:    python3-oslo-vmware
BuildRequires:    python3-os-win
BuildRequires:    python3-castellan
BuildRequires:    python3-cryptography
BuildRequires:    python3-osprofiler
BuildRequires:    python3-paramiko
BuildRequires:    python3-suds
BuildRequires:    python3-taskflow
BuildRequires:    python3-tooz
BuildRequires:    python3-oslo-log
BuildRequires:    python3-oslo-i18n
BuildRequires:    python3-barbicanclient
BuildRequires:    python3-requests
BuildRequires:    python3-defusedxml

# Required to compile translation files
BuildRequires:    python3-babel

# Needed for unit tests
BuildRequires:    python3-ddt
BuildRequires:    python3-fixtures
BuildRequires:    python3-mock
BuildRequires:    python3-oslotest
BuildRequires:    python3-subunit
BuildRequires:    python3-testtools
BuildRequires:    python3-testrepository
BuildRequires:    python3-testresources
BuildRequires:    python3-testscenarios
BuildRequires:    python3-os-testr
BuildRequires:    python3-tabulate

BuildRequires:    python3-decorator
BuildRequires:    python3-lxml
BuildRequires:    python3-retrying
BuildRequires:    python3-rtslib


Requires:         python3-%{service} = %{epoch}:%{version}-%{release}

# we dropped the patch to remove PBR for Delorean
Requires:         python3-pbr

# as convenience
Requires:         python3-cinderclient

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
Requires(pre):    shadow-utils

Requires:         lvm2
Requires:         python3-osprofiler

Requires:         python3-rtslib
Requires:         python3-pyudev


%description
%{common_desc}


%package -n       python3-%{service}
Summary:          OpenStack Volume Python libraries
%{?python_provide:%python_provide python3-%{service}}
Group:            Applications/System

Requires:         sudo

Requires:         cryptsetup
Requires:         cracklib-dicts
Requires:         qemu-img >= 2.10.0
Requires:         sysfsutils
Requires:         python3-paramiko >= 2.4.0
Requires:         python3-jsonschema >= 2.6.0

Requires:         python3-castellan >= 0.16.0
Requires:         python3-cursive >= 0.2.1
Requires:         python3-etcd3gw
Requires:         python3-eventlet >= 0.22.0
Requires:         python3-greenlet >= 0.4.10
Requires:         python3-iso8601 >= 0.1.11
Requires:         python3-stevedore >= 1.20.0
Requires:         python3-tooz >= 1.58.0

Requires:         python3-sqlalchemy >= 1.0.10
Requires:         python3-routes >= 2.3.1
Requires:         python3-webob >= 1.7.1

Requires:         python3-barbicanclient >= 4.5.2
Requires:         python3-glanceclient >= 1:2.15.0
Requires:         python3-keystoneclient >= 1:3.15.0
Requires:         python3-novaclient >= 9.1.0
Requires:         python3-swiftclient >= 3.2.0

Requires:         python3-six >= 1.10.0
Requires:         python3-psutil >= 3.2.2

Requires:         python3-google-api-client >= 1.4.2

Requires:         python3-keystonemiddleware >= 4.21.0
Requires:         python3-keystoneauth1 >= 3.7.0
Requires:         python3-osprofiler >= 1.4.0
Requires:         python3-os-brick >= 2.2.0
Requires:         python3-os-win >= 3.0.0
Requires:         python3-oslo-config >= 2:5.2.0
Requires:         python3-oslo-concurrency >= 3.26.0
Requires:         python3-oslo-context >= 2.19.2
Requires:         python3-oslo-db >= 4.35.0
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-oslo-log >= 3.36.0
Requires:         python3-oslo-middleware >= 3.31.0
Requires:         python3-oslo-messaging >= 6.4.0
Requires:         python3-oslo-policy >= 1.44.1
Requires:         python3-oslo-privsep >= 1.32.0
Requires:         python3-oslo-reports >= 1.18.0
Requires:         python3-oslo-rootwrap >= 5.8.0
Requires:         python3-oslo-serialization >= 2.18.0
Requires:         python3-oslo-service >= 1.24.0
Requires:         python3-oslo-upgradecheck >= 0.1.0
Requires:         python3-oslo-utils >= 3.34.0
Requires:         python3-oslo-versionedobjects >= 1.31.2
Requires:         python3-oslo-vmware >= 2.35.0
Requires:         python3-taskflow >= 3.2.0

Requires:         iscsi-initiator-utils

Requires:         python3-oauth2client >= 1.5.0
Requires:         python3-requests >= 2.14.2
Requires:         python3-pyparsing >= 2.1.0
Requires:         python3-pytz
Requires:         python3-tabulate >= 0.8.5

Requires:         python3-cryptography >= 2.1

Requires:         python3-defusedxml >= 0.5.0

Requires:         python3-lxml >= 3.4.1
Requires:         python3-migrate >= 0.11.0
Requires:         python3-paste
Requires:         python3-paste-deploy
Requires:         python3-httplib2 >= 0.9.1
Requires:         python3-retrying >= 1.2.3
Requires:         python3-decorator

# Required by the volume_copy_bps_limit option
# at least where the package is available
%if 0%{?rhel} && 0%{?rhel} < 9
Requires:         libcgroup-tools
%endif


%description -n   python3-%{service}
%{common_desc}

This package contains the %{service} Python library.

%package -n python3-%{service}-tests
Summary:        Cinder tests
%{?python_provide:%python_provide python3-%{service}-tests}
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

# Added test requirements
Requires:       python3-hacking
Requires:       python3-ddt
Requires:       python3-fixtures
Requires:       python3-mock
Requires:       python3-oslotest
Requires:       python3-subunit
Requires:       python3-testtools
Requires:       python3-testrepository
Requires:       python3-testresources
Requires:       python3-testscenarios
Requires:       python3-stestr


%description -n python3-%{service}-tests
%{common_desc}

This package contains the Cinder test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Volume
Group:            Documentation

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    graphviz
BuildRequires:    python3-sphinx
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-sphinxcontrib-apidoc
BuildRequires:    python3-sphinx-feature-classification
# Required to build module documents
BuildRequires:    python3-eventlet
BuildRequires:    python3-routes
BuildRequires:    python3-sqlalchemy
BuildRequires:    python3-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python3-iso8601 >= 0.1.9

BuildRequires:    python3-migrate


%description      doc
%{common_desc}

This package contains documentation files for %{service}.
%endif

%prep
%autosetup -n %{service}-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +
sed -i 's/\/usr\/bin\/env python/\/usr\/bin\/env python3/' tools/generate_driver_list.py

sed -i 's/%{version}.%{milestone}/%{version}/' PKG-INFO

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=tools/config/%{service}-config-generator.conf

# Build
%{py3_build}

# Generate i18n files
# (amoralej) we can remove '-D cinder' once https://review.openstack.org/#/c/439501/ is merged
%{__python3} setup.py compile_catalog -d build/lib/%{service}/locale -D cinder

%install
%{py3_install}

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
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python3_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

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

%files -n python3-%{service} -f %{service}.lang
%{?!_licensedir: %global license %%doc}
%license LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.egg-info
%exclude %{python3_sitelib}/%{service}/test.py
%exclude %{python3_sitelib}/%{service}/tests

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/test.py
%{python3_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
* Mon Nov 15 2021 RDO <dev@lists.rdoproject.org> 1:16.4.2-1
- Update to 16.4.2

* Thu Sep 23 2021 RDO <dev@lists.rdoproject.org> 1:16.4.1-1
- Update to 16.4.1

* Thu Jul 29 2021 RDO <dev@lists.rdoproject.org> 1:16.4.0-1
- Update to 16.4.0

* Thu Mar 11 2021 RDO <dev@lists.rdoproject.org> 1:16.3.0-1
- Update to 16.3.0

* Tue Dec 08 2020 RDO <dev@lists.rdoproject.org> 1:16.2.1-1
- Update to 16.2.1

* Wed Sep 30 2020 RDO <dev@lists.rdoproject.org> 1:16.2.0-1
- Update to 16.2.0

* Mon Jun 08 2020 RDO <dev@lists.rdoproject.org> 1:16.1.0-1
- Update to 16.1.0

* Wed May 13 2020 RDO <dev@lists.rdoproject.org> 1:16.0.0-1
- Update to 16.0.0

* Fri May 08 2020 RDO <dev@lists.rdoproject.org> 1:16.0.0-0.3.0rc2
- Update to 16.0.0.0rc3

* Mon May 04 2020 RDO <dev@lists.rdoproject.org> 1:16.0.0-0.2.0rc1
- Update to 16.0.0.0rc2

* Wed Apr 29 2020 RDO <dev@lists.rdoproject.org> 1:16.0.0-0.1.0rc1
- Update to 16.0.0.0rc1

