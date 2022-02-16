%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x4c29ff0e437f3351fd82bdf47c5a3bc787dc7035
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
Version:          19.0.0
Release:          2%{?dist}
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif


BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
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
BuildRequires:    python3-keystonemiddleware
BuildRequires:    python3-glanceclient >= 1:3.2.2
BuildRequires:    python3-novaclient >= 17.0.0
BuildRequires:    python3-swiftclient >= 3.10.1
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
BuildRequires:    python3-boto3

# Required to compile translation files
BuildRequires:    python3-babel

%if 0%{?rhosp} == 0
# Google Backup driver
BuildRequires:    python3-google-api-client
%endif

# Needed for unit tests
BuildRequires:    python3-ddt
BuildRequires:    python3-fixtures
BuildRequires:    python3-mock
BuildRequires:    python3-oslotest
BuildRequires:    python3-packaging
BuildRequires:    python3-subunit
BuildRequires:    python3-testtools
BuildRequires:    python3-testrepository
BuildRequires:    python3-testresources
BuildRequires:    python3-testscenarios
BuildRequires:    python3-os-testr
BuildRequires:    python3-tabulate

BuildRequires:    python3-decorator
BuildRequires:    python3-lxml
BuildRequires:    python3-rtslib
BuildRequires:    python3-tenacity


Requires:         python3-%{service} = %{epoch}:%{version}-%{release}

# we dropped the patch to remove PBR for Delorean
Requires:         python3-pbr >= 5.5.1

# as convenience
Requires:         python3-cinderclient

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
Requires(pre):    shadow-utils

Requires:         python3-osprofiler

Requires:         python3-pyudev

%description
%{common_desc}


%package -n       python3-%{service}
Summary:          OpenStack Volume Python libraries
%{?python_provide:%python_provide python3-%{service}}
Group:            Applications/System

Requires:         python3-%{service}-common = %{epoch}:%{version}-%{release}

Requires:         cryptsetup
Requires:         cracklib-dicts
Requires:         qemu-img >= 2.10.0
Requires:         python3-jsonschema >= 3.2.0

Requires:         python3-castellan >= 3.6.0
Requires:         python3-cursive >= 0.2.2
Requires:         python3-etcd3gw

Requires:         python3-routes >= 2.4.1
Requires:         python3-webob >= 1.8.6

Requires:         python3-barbicanclient >= 5.0.1
Requires:         python3-glanceclient >= 1:3.2.2
Requires:         python3-keystoneclient >= 1:4.1.1
Requires:         python3-novaclient >= 17.2.1
Requires:         python3-swiftclient >= 3.10.1

Requires:         python3-keystonemiddleware >= 9.1.0
Requires:         python3-keystoneauth1 >= 4.2.1
Requires:         python3-osprofiler >= 3.4.0

Requires:         python3-os-win >= 5.4.0

Requires:         python3-oslo-middleware >= 4.1.1
Requires:         python3-oslo-messaging >= 12.5.0
Requires:         python3-oslo-policy >= 3.6.2
Requires:         python3-oslo-reports >= 2.2.0
Requires:         python3-oslo-upgradecheck >= 1.1.1
Requires:         python3-oslo-vmware >= 3.8.0

Requires:         python3-packaging >= 20.4
Requires:         python3-paste >= 3.4.3
Requires:         python3-paste-deploy >= 2.1.0

%if 0%{?rhosp} == 0
# Google Backup driver
Requires:         python3-google-api-client
Requires:         python3-oauth2client >= 4.1.3
%endif

%description -n   python3-%{service}
%{common_desc}

This package contains the %{service} Python library.

%package -n python3-%{service}-common
# This package contains Cinder python code, but does not track dependencies
# for all of Cinder.  Dependencies here are intended only to make it possible
# to load and use Cinder drivers and not the Cinder service.
Summary:        Cinder common code
%{?python_provide:%python_provide python3-%{service}-common}

Requires:         sudo

Requires:         python3-paramiko >= 2.7.2

Requires:         python3-eventlet >= 0.30.1
Requires:         python3-greenlet >= 0.4.13
Requires:         python3-iso8601 >= 0.1.12
Requires:         python3-stevedore >= 3.2.2
Requires:         python3-tooz >= 2.7.1

Requires:         python3-sqlalchemy >= 1.3.2

Requires:         python3-six >= 1.15.0
Requires:         python3-psutil >= 5.7.2

Requires:         python3-os-brick >= 4.3.1
Requires:         python3-oslo-config >= 2:8.3.2
Requires:         python3-oslo-concurrency >= 4.4.0
Requires:         python3-oslo-context >= 3.1.1
Requires:         python3-oslo-db >= 8.4.0
Requires:         python3-oslo-i18n >= 5.0.1
Requires:         python3-oslo-log >= 4.5.0
Requires:         python3-oslo-privsep >= 2.4.0
Requires:         python3-oslo-rootwrap >= 6.2.0
Requires:         python3-oslo-serialization >= 4.1.0
Requires:         python3-oslo-service >= 2.5.0
Requires:         python3-oslo-utils >= 4.8.0
Requires:         python3-oslo-versionedobjects >= 2.3.0
Requires:         python3-zstd >= 1.4.5.1
Requires:         python3-boto3
%if 0%{?rhel} && 0%{?rhel} < 9
Requires:         python3-importlib-metadata >= 1.7.0
%endif

# Required by 3PAR and VNX as well as cinder flows
Requires:         python3-taskflow >= 4.5.0

Requires:         iscsi-initiator-utils
Requires:         nvmetcli

Requires:         python3-requests >= 2.25.1
Requires:         python3-pyparsing >= 2.4.6
Requires:         python3-pytz
Requires:         python3-tabulate >= 0.8.7

Requires:         python3-cryptography >= 3.1


Requires:         python3-lxml >= 4.2.3
Requires:         python3-migrate >= 0.13.0
Requires:         python3-httplib2 >= 0.16.0
Requires:         python3-tenacity >= 6.2.0
Requires:         python3-decorator

# Required by LVM-LIO
Requires:         lvm2
Requires:         python3-rtslib >= 2.1.74
Requires:         targetcli

# Required by the volume_copy_bps_limit option
# at least where the package is available
%if 0%{?rhel} && 0%{?rhel} < 9
Requires:         libcgroup-tools
%endif


%description -n   python3-%{service}-common
Common code for Cinder.

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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

%exclude %{_bindir}/%{service}-rtstool
%{_bindir}/%{service}-*
%{_unitdir}/*.service
%{_datarootdir}/%{service}
%if 0%{?with_doc}
%{_mandir}/man1/%{service}*.1.gz
%endif

%defattr(-, %{service}, %{service}, -)
%dir %{_sharedstatedir}/%{service}
%dir %{_sharedstatedir}/%{service}/tmp

%files -n python3-%{service}

%files -n python3-%{service}-common -f %{service}.lang
%license LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.egg-info
%{_bindir}/%{service}-rtstool
%exclude %{python3_sitelib}/%{service}/tests

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
* Wed Feb 16 2022 Tobias Urdin <tobias.urdin@binero.com> 1:19.0.0-2
- Update oslo.log requires to >= 4.5.0

* Wed Oct 06 2021 RDO <dev@lists.rdoproject.org> 1:19.0.0-1
- Update to 19.0.0

* Fri Oct 01 2021 RDO <dev@lists.rdoproject.org> 1:19.0.0-0.2.0rc1
- Update to 19.0.0.0rc2

* Fri Sep 17 2021 RDO <dev@lists.rdoproject.org> 1:19.0.0-0.1.0rc1
- Update to 19.0.0.0rc1

