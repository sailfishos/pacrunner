Name:		pacrunner
Version:	0.3
Release:	3%{?dist}
Summary:	Proxy configuration dæmon

Group:		System/Networking
License:	GPLv2
URL:		http://connman.net/
Source0:	http://www.kernel.org/pub/linux/network/connman/pacrunner-%{version}.tar.bz2
Source1:	libproxy.py
BuildRequires:	python v8-devel
BuildRequires:	pkgconfig(glib-2.0) pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gthread-2.0) pkgconfig(libcurl)
Obsoletes:	libproxy < 0.5
Provides:	libproxy

%description
PacRunner provides a dæmon for processing proxy configuration
and providing information to clients over D-Bus.

%package devel
Summary:    Development files for PacRunner
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Obsoletes:  libproxy-devel < 0.5
Provides:   libproxy-devel
%description devel
This provides the development files for building against
pacrunner's implementation of libproxy

%package python
Summary:    Python lib for PacRunner
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pacrunner
Obsoletes:  libproxy-python < 0.5
Provides:   libproxy-python
%description python
A python library for proxy configuration and autodetection

%prep
%setup -q

%build
autoreconf --force --install
%configure --enable-libproxy --enable-curl --disable-capng --enable-datafiles --enable-v8
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/%{_datadir}/dbus-1/system-services/{,org.}pacrunner.service
mkdir -p ${RPM_BUILD_ROOT}/%{python_sitelib}
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT/%{python_sitelib}/libproxy.py
rm -f $RPM_BUILD_ROOT/%{_libdir}/libproxy.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README COPYING.LIB AUTHORS ChangeLog
%{_sbindir}/pacrunner
%{_libdir}/libproxy.so.1.0.0
%{_libdir}/libproxy.so.1
%{_bindir}/proxy
%{_datadir}/dbus-1/system-services/org.pacrunner.service
%config %{_sysconfdir}/dbus-1/system.d/pacrunner.conf

%files devel
%{_libdir}/libproxy.so
/usr/include/proxy.h
%{_libdir}/pkgconfig/libproxy-1.0.pc

%files python
%{python_sitelib}/libproxy.py*
