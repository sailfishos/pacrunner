Name:       pacrunner

Summary:    Proxy configuration daemon
Version:    0.15
Release:    1
License:    GPLv2+
URL:        https://git.sailfishos.org/mer-core/pacrunner/
Source0:    http://www.kernel.org/pub/linux/network/connman/pacrunner-%{version}.tar.xz
Source1:    libproxy.py
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  libtool
BuildRequires:  python3-devel
Provides:   libproxy
Obsoletes:   libproxy < 0.5
Conflicts:   pacrunner-cutes
Obsoletes:   pacrunner-cutes

Patch1: 0001-Use-systemd-activation-for-dbus.-Contributes-to-JB-2.patch

%description
PacRunner provides a daemon for processing proxy configuration
and providing information to clients over D-Bus.

%package python
Summary:    Python lib for PacRunner
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pacrunner
Provides:   libproxy-python
Obsoletes:   libproxy-python < 0.5

%description python
A python library for proxy configuration and autodetection

%package devel
Summary:    Development files for PacRunner
Requires:   %{name} = %{version}-%{release}
Provides:   libproxy-devel
Obsoletes:   libproxy-devel < 0.5

%description devel
This provides the development files for building against
pacrunner's implementation of libproxy

%package test
Summary:    Test files for PacRunner
Requires:   %{name} = %{version}-%{release}

%description test
This provides the test files for pacrunner


%package doc
Summary:    Documentation for %{name}
Requires:   %{name} = %{version}-%{release}

%description doc
%{summary}.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch1 -p1

%build
./bootstrap

%configure --disable-static \
    --enable-libproxy \
    --enable-curl \
    --enable-datafiles \
    --enable-duktape \
    --with-systemdunitdir=%{_unitdir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

mkdir -p ${RPM_BUILD_ROOT}/%{python3_sitelib}
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT/%{python3_sitelib}/libproxy.py
rm -f $RPM_BUILD_ROOT/%{_libdir}/libproxy.la

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
install -m0644 -t $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version} \
        README AUTHORS ChangeLog

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LIB
%{_sbindir}/pacrunner
%{_libdir}/libproxy.so.1.0.0
%{_libdir}/libproxy.so.1
%{_bindir}/proxy
%{_datadir}/dbus-1/system-services/org.pacrunner.service
%{_unitdir}/dbus-org.pacrunner.service
%config %{_sysconfdir}/dbus-1/system.d/pacrunner.conf

%files python
%defattr(-,root,root,-)
%{python3_sitelib}/libproxy.py*
%{python3_sitelib}/__pycache__/libproxy.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libproxy.so
%{_includedir}/proxy.h
%{_libdir}/pkgconfig/libproxy-1.0.pc

%files test
%defattr(-,root,root,-)
%{_bindir}/manual-proxy-test

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}
