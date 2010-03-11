%define name	upower
%define oname	UPower
%define version	0.9.1
%define release	%mkrel 1
%define major 1
%define libname %mklibname upower-glib %major
%define develname %mklibname -d upower-glib
%define oldlibname %mklibname devkit-power-gobject 1
%define olddevelname %mklibname -d devkit-power-gobject

%define git_url git://anongit.freedesktop.org/DeviceKit/upower

Name: %name
Version: %version
Release: %release
Summary: Power Management Service
License: GPLv2+
Group: System/Kernel and hardware
URL: http://hal.freedesktop.org/releases/
Source0: http://hal.freedesktop.org/releases/%{oname}-%{version}.tar.bz2
BuildRoot: %_tmppath/%name-%version-%release-root
Provides: %{oname} = %{version}-%{release}
BuildRequires: libgudev-devel
BuildRequires: glib2-devel 
BuildRequires: dbus-devel 
BuildRequires: dbus-glib-devel
BuildRequires: polkit-1-devel >= 0.91
BuildRequires: sqlite-devel
BuildRequires: libtool
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: libusb-devel
BuildRequires: libxslt-proc
BuildRequires: docbook-style-xsl
BuildRequires: gtk-doc >= 1.3
Requires: pm-utils
Obsoletes: devicekit-power < 014-2
Provides: devicekit-power = 014-2

%description
%{oname} provides a daemon, API and command line tools for
managing power devices attached to the system.

%package -n %libname
Summary: Shared Library of %{oname}
Group: System/Libraries
Requires: %name >= %version-%release
Obsoletes: %oldlibname < 014-2

%description -n %libname
%{oname} provides a daemon, API and command line tools for
managing power devices attached to the system.


%package -n %develname
Summary: Headers and libraries for %{oname}
Group: Development/C
Provides: %{oname}-devel = %{version}-%{release}
Requires: %{name} = %{version}
Requires: %libname = %version-%release
#gw libtool dep
Requires: libusb-devel
Obsoletes: %olddevelname < 014-2

%description -n %develname
Headers and libraries for %{oname}

%prep
%setup -q -n %{oname}-%{version}

%build
%configure2_5x --enable-gtk-doc
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang UPower

%clean
rm -rf %{buildroot}

%files -f UPower.lang
%defattr(-,root,root,-)

%doc README AUTHORS NEWS COPYING HACKING

%{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules

%{_bindir}/*
%{_libdir}/devkit-power-daemon
%{_libdir}/upowerd

%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/*.so.%{major}*

%files -n %develname
%{_datadir}/dbus-1/interfaces/*.xml
%dir %{_datadir}/gtk-doc/html/UPower
%{_datadir}/gtk-doc/html/UPower/*
%{_includedir}/DeviceKit-power/devkit-power-gobject/
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/gir-1.0/*.gir
%{_includedir}/libupower-glib

