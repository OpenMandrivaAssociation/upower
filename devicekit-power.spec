%define name	devicekit-power
%define oname	DeviceKit-power
%define version	014
%define release	%mkrel 1
%define major 1
%define libname %mklibname devkit-power-gobject %major
%define develname %mklibname -d devkit-power-gobject

%define git_url git://anongit.freedesktop.org/DeviceKit/DeviceKit-power

Name: %name
Version: %version
Release: %release
Summary: Power Management Service
License: GPLv2+
Group: System/Kernel and hardware
URL: http://gitweb.freedesktop.org/?p=users/david/DeviceKit.git;a=summary
Source0: http://hal.freedesktop.org/releases/%{oname}-%{version}.tar.gz
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

%description
DeviceKit-power provides a daemon, API and command line tools for
managing power devices attached to the system.

%package -n %libname
Summary: Shared Library of DeviceKit-power
Group: System/Libraries
Requires: %name >= %version-%release
Conflicts: %name < 008-2mdv

%description -n %libname
DeviceKit-power provides a daemon, API and command line tools for
managing power devices attached to the system.


%package -n %develname
Summary: Headers and libraries for DeviceKit-power
Group: Development/C
Provides: %{oname}-devel = %{version}-%{release}
Provides: %name-devel = %version-%release
Obsoletes: %name-devel
Requires: %{name} = %{version}
Requires: %libname = %version-%release
#gw libtool dep
Requires: libusb-devel

%description -n %develname
Headers and libraries for DeviceKit-power.

%prep
%setup -q -n %{oname}-%{version}

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%doc README AUTHORS NEWS COPYING HACKING doc/TODO

%{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules

%{_bindir}/*
%{_libdir}/devkit-power-daemon

%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/libdevkit-power-gobject.so.%{major}*

%files -n %develname
%{_datadir}/dbus-1/interfaces/*.xml
%dir %{_datadir}/gtk-doc/html/devkit-power
%{_datadir}/gtk-doc/html/devkit-power/*
%{_includedir}/DeviceKit-power/devkit-power-gobject/
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
