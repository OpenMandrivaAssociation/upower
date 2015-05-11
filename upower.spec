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
Version:	0.99.2
Release:	2
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://upower.freedesktop.org/
Source0:	http://upower.freedesktop.org/releases/%{name}-%{version}.tar.xz
#Patch0:		0001-lib-Fix-segfault-on-getting-property-when-daemon-is-.patch

BuildRequires:	docbook-style-xsl
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gudev-1.0) >= 186
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libimobiledevice-1.0)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	systemd-units >= 37
BuildRequires:	pkgconfig(systemd)
Requires(post,preun,postun):	systemd-units
Requires(post,preun):	rpm-helper
Requires(post):	systemd-sysvinit
# As i know now suspend provides by systemd
# systemd for suspend and hibernate 
# fedya
Requires:	polkit
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

%description -n	%{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Headers and libraries for %{oname}
Group:		Development/C
Provides:	%{oname}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{olddevname}

%description -n	%{devname}
Headers and libraries for %{oname}.

%prep
%setup -q
%apply_patches

%build
%configure \
	--enable-gtk-doc \
	--enable-introspection

%make

%install
%makeinstall_std

%find_lang %{name}

%post
%systemd_post %{name}

%preun
%systemd_postun %{name}

%files -f %{name}.lang
%doc README AUTHORS NEWS HACKING
%dir %{_sysconfdir}/UPower/
%config(noreplace) %{_sysconfdir}/UPower/UPower.conf
%{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules
%{_localstatedir}/lib/upower
%{_bindir}/*
%{_libexecdir}/upowerd
#% {_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service
%{_unitdir}/upower.service
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

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
