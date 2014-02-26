# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.24
# 

Name:       pacrunner

# >> macros
# << macros

Summary:    Proxy configuration daemon
Version:    0.8
Release:    1
Group:      System/Networking
License:    GPLv2
URL:        http://connman.net/
Source0:    http://www.kernel.org/pub/linux/network/connman/pacrunner-%{version}.tar.xz
Source1:    libproxy.py
Source2:    http://www.kernel.org/pub/linux/network/connman/pacrunner-%{version}.tar.sign
Source100:  pacrunner.yaml
Patch0:     pacrunner-0.8-plugins-Do-not-try-to-resolve.patch
Patch1:     pacrunner-0.8-plugins-Update-v8-plugin-to-the-newest-API.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  python
BuildRequires:  v8-devel
BuildRequires:  pkgconfig(gthread-2.0)
Provides:   libproxy
Obsoletes:   libproxy < 0.5

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
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:   libproxy-devel
Obsoletes:   libproxy-devel < 0.5

%description devel
This provides the development files for building against
pacrunner's implementation of libproxy


%package test
Summary:    Test files for PacRunner
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description test
This provides the test files for pacrunner



%prep
%setup -q -n %{name}-%{version}

# pacrunner-0.8-plugins-Do-not-try-to-resolve.patch
%patch0 -p1
# pacrunner-0.8-plugins-Update-v8-plugin-to-the-newest-API.patch
%patch1 -p1
# >> setup
# << setup

%build
# >> build pre
autoreconf --force --install
# << build pre

%configure --disable-static \
    --enable-libproxy \
    --enable-curl \
    --disable-capng \
    --enable-datafiles \
    --enable-v8

make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
mv $RPM_BUILD_ROOT/%{_datadir}/dbus-1/system-services/{,org.}pacrunner.service
mkdir -p ${RPM_BUILD_ROOT}/%{python_sitelib}
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT/%{python_sitelib}/libproxy.py
rm -f $RPM_BUILD_ROOT/%{_libdir}/libproxy.la
# << install post


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
# >> files
%doc COPYING README COPYING.LIB AUTHORS ChangeLog
%{_sbindir}/pacrunner
%{_libdir}/libproxy.so.1.0.0
%{_libdir}/libproxy.so.1
%{_bindir}/proxy
%{_datadir}/dbus-1/system-services/org.pacrunner.service
%config %{_sysconfdir}/dbus-1/system.d/pacrunner.conf
# << files

%files python
%defattr(-,root,root,-)
# >> files python
%{python_sitelib}/libproxy.py*
# << files python

%files devel
%defattr(-,root,root,-)
# >> files devel
%{_libdir}/libproxy.so
%{_includedir}/proxy.h
%{_libdir}/pkgconfig/libproxy-1.0.pc
# << files devel

%files test
%defattr(-,root,root,-)
# >> files test
%{_bindir}/manual-proxy-test
# << files test
