%define oname UPower

%define major 3
%define girmajor 1.0
%define libname %mklibname upower-glib %{major}
%define girname %mklibname upower-glib-gir %{girmajor}
%define devname %mklibname -d upower-glib

%define oldlibname %mklibname devkit-power-gobject 1
%define olddevname %mklibname -d devkit-power-gobject

Summary:	Power Management Service
Name:		upower
Version:	1.90.7
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		https://upower.freedesktop.org/
Source0:	https://gitlab.freedesktop.org/upower/%{name}/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	xsltproc
BuildRequires:	meson
BuildRequires:	pkgconfig(gudev-1.0) >= 186
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libimobiledevice-1.0)
BuildRequires:	python3dist(python-dbusmock)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-rpm-macros
# As i know now suspend provides by systemd
# systemd for suspend and hibernate
# fedya
Requires:	udev
Requires:	gobject-introspection
Provides:	%{oname} = %{version}-%{release}
%rename		devicekit-power

%description
%{oname} provides a daemon, API and command line tools for
managing power devices attached to the system.

%package -n %{libname}
Summary:	Shared Library of %{oname}
Group:		System/Libraries
Obsoletes:	%{oldlibname}

%description -n %{libname}
%{oname} provides a daemon, API and command line tools for
managing power devices attached to the system.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}upower-glib1 < 0.9.15-3

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Headers and libraries for %{oname}
Group:		Development/C
Provides:	%{oname}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{olddevname}

%description -n %{devname}
Headers and libraries for %{oname}.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%meson \
  -Dman=true \
  -Dgtk-doc=true \
  -Dintrospection=enabled

%meson_build

%install
%meson_install

%find_lang %{name}

%post
%systemd_post upower.service
 
%preun
%systemd_preun upower.service
 
%postun
%systemd_postun_with_restart upower.service

%files -f %{name}.lang
%doc README AUTHORS NEWS HACKING
%dir %{_sysconfdir}/UPower/
%config(noreplace) %{_sysconfdir}/UPower/UPower.conf
%{_datadir}/dbus-1/system.d/*.conf
%{_udevrulesdir}/*.rules
%{_udevhwdbdir}/*.hwdb
%{_localstatedir}/lib/upower
%{_bindir}/*
%{_libexecdir}/upowerd
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%{_datadir}/dbus-1/system-services/*.service
%{_unitdir}/upower.service
%dir %{_datadir}/installed-tests/%{name}
%{_datadir}/installed-tests/%{name}/*test
%doc %{_mandir}/man1/*
%doc %{_mandir}/man7/*
%doc %{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/libupower-glib.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/UPowerGlib-%{girmajor}.typelib

%files -n %{devname}
%{_includedir}/libupower-glib
%{_libdir}/*.so
%{_libdir}/pkgconfig/upower-glib.pc
%{_datadir}/dbus-1/interfaces/*.xml
%dir %{_datadir}/gtk-doc/html/UPower
%{_datadir}/gtk-doc/html/UPower/*
%{_datadir}/gir-1.0/UPowerGlib-%{girmajor}.gir
