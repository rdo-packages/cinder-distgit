%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some runtime reqs from automatic generator when rhosp != 0
%if 0%{?rhosp}
# Google Backup driver
%global excluded_reqs google-api-python-client oauth2client
%endif
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8 moto mypy
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
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
Version:          XXX
Release:          XXX
Summary:          OpenStack Volume service

License:          Apache-2.0
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
BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    systemd
BuildRequires:    git-core
BuildRequires:    openstack-macros

# Required to build cinder.conf
BuildRequires:    python3-certifi

Requires:         python3-%{service} = %{epoch}:%{version}-%{release}
# as convenience
Requires:         python3-cinderclient

%{?systemd_ordering}

Requires(pre):    shadow-utils

%description
%{common_desc}


%package -n       python3-%{service}
Summary:          OpenStack Volume Python libraries
Group:            Applications/System

Requires:         python3-%{service}-common = %{epoch}:%{version}-%{release}

Requires:         cryptsetup
Requires:         qemu-img >= 2.10.0

%description -n   python3-%{service}
%{common_desc}

This package contains the %{service} Python library.

%package -n python3-%{service}-common
# This package contains Cinder python code, but does not track dependencies
# for all of Cinder.  Dependencies here are intended only to make it possible
# to load and use Cinder drivers and not the Cinder service.
Summary:        Cinder common code

Requires:         sudo
Requires:         iscsi-initiator-utils
Requires:         nvmetcli

# Required by LVM-LIO
Requires:         lvm2
Requires:         targetcli

# Required by DataCore driver
Requires:         python3-websocket-client

%description -n   python3-%{service}-common
Common code for Cinder.

%package -n python3-%{service}-tests
Summary:        Cinder tests
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

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Remove syntax check test
rm -f cinder/tests/unit/test_hacking.py
# python-moto is not available
rm -f cinder/tests/unit/backup/drivers/test_backup_s3.py

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
# Exclude some bad-known runtime reqs
for pkg in %{excluded_reqs}; do
  sed -i /^${pkg}.*/d requirements.txt
done

%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
# Build
%pyproject_wheel

# Generate i18n files

%install
%pyproject_install

# Generate i18n files
%{__python3} setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/%{service}/locale -D cinder

# Generate config file
PYTHONPATH="%{buildroot}/%{python3_sitelib}" oslo-config-generator --config-file=tools/config/%{service}-config-generator.conf

%if 0%{?with_doc}
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
sphinx-build -W -b man doc/source doc/build/man
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
%check
%tox -e %{default_toxenv}

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
%{python3_sitelib}/%{service}-*.dist-info
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
