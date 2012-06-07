%define oname	UPower

%define major 1
%define girmajor 1.0
%define libname %mklibname upower-glib %{major}
%define girname %mklibname upower-glib-gir %{girmajor}
%define develname %mklibname -d upower-glib

%define oldlibname %mklibname devkit-power-gobject 1
%define olddevelname %mklibname -d devkit-power-gobject

%bcond_without	systemd

Summary:	Power Management Service
Name:		upower
Version:	0.9.16
Release:	3
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://upower.freedesktop.org/
Source0:	http://upower.freedesktop.org/releases/%{name}-%{version}.tar.xz
Source1:	upowerd.service
Patch0:		upower-0.9.15-add-gmodule-link.patch

BuildRequires:	docbook-style-xsl
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libimobiledevice-1.0)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(polkit-gobject-1)
%if %{with systemd}
BuildRequires:	systemd-units >= 37
Requires(post,preun,postun): systemd-units
Requires(post):	systemd-sysvinit
%endif

Requires:	pm-utils
Requires:	suspend
Provides:	%{oname} = %{version}-%{release}
Obsoletes:	devicekit-power

%description
%{oname} provides a daemon, API and command line tools for
managing power devices attached to the system.

%package -n	%{libname}
Summary:	Shared Library of %{oname}
Group:		System/Libraries
Obsoletes:	%{oldlibname}

%description -n %{libname}
%{oname} provides a daemon, API and command line tools for
managing power devices attached to the system.

%package -n	%{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}upower-glib1 < 0.9.15-3

%description -n	%{girname}
GObject Introspection interface description for %{name}.

%package -n	%{develname}
Summary:	Headers and libraries for %{oname}
Group:		Development/C
Provides:	%{oname}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}
Obsoletes:	%{olddevelname}

%description -n	%{develname}
Headers and libraries for %{oname}

%prep
%setup -q
%apply_patches

%build
libtoolize --copy --force
autoreconf

%configure2_5x \
	--disable-dependency-tracking \
	--enable-gtk-doc \
	--disable-static

%make

%install
%makeinstall_std

%if %{with systemd}
install -m644 %{SOURCE1} -D %{buildroot}%{_unitdir}/upowerd.service
sed -e 's#/usr/lib/#%{_libexecdir}#g' -i %{buildroot}%{_unitdir}/upowerd.service
%endif

%find_lang %{name} %{name}.lang

%if %{with systemd}
%post 	 
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ "$1" -ge 1 ]; then
	/bin/systemctl enable upowerd.service >/dev/null 2>&1 || :
	/bin/systemctl try-restart upowerd.service >/dev/null 2>&1 || :
fi
 
%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ "$1" -ge 1 ] ; then
	/bin/systemctl try-restart upowerd.service >/dev/null 2>&1 || :
fi
 
%preun
if [ "$1" = "0" ]; then
	/bin/systemctl --no-reload upowerd.service > /dev/null 2>&1 || :
	/bin/systemctl stop upowerd.service > /dev/null 2>&1 || :
fi
%endif

%files -f %{name}.lang
%doc README AUTHORS NEWS HACKING
%dir %{_sysconfdir}/UPower/
%config(noreplace) %{_sysconfdir}/UPower/UPower.conf
%{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules
%{_localstatedir}/lib/upower
%{_bindir}/*
%{_libexecdir}/upowerd
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service
%if %{with systemd}
%{_unitdir}/upowerd.service
%endif
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/libupower-glib.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/UPowerGlib-%{girmajor}.typelib

%files -n %{develname}
%{_includedir}/libupower-glib
%{_libdir}/*.so
%{_libdir}/pkgconfig/upower-glib.pc
%{_datadir}/dbus-1/interfaces/*.xml
%dir %{_datadir}/gtk-doc/html/UPower
%{_datadir}/gtk-doc/html/UPower/*
%{_datadir}/gir-1.0/UPowerGlib-%{girmajor}.gir
