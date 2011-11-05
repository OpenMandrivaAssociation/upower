%define _with_systemd 1

%define name	upower
%define oname	UPower
%define version	0.9.14
%define release	%mkrel 7
%define major 1
%define libname %mklibname upower-glib %major
%define develname %mklibname -d upower-glib
%define oldlibname %mklibname devkit-power-gobject 1
%define olddevelname %mklibname -d devkit-power-gobject

Name: %name
Version: %version
Release: %release
Summary: Power Management Service
License: GPLv2+
Group: System/Kernel and hardware
URL:     http://upower.freedesktop.org/
Source0: http://upower.freedesktop.org/releases/%{name}-%{version}.tar.xz
Source1: upowerd.service
Provides: %{oname} = %{version}-%{release}
BuildRequires: libgudev-devel
BuildRequires: dbus-glib-devel
BuildRequires: polkit-1-devel >= 0.91
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: libusb-devel
BuildRequires: libxslt-proc
BuildRequires: docbook-style-xsl
BuildRequires: gobject-introspection-devel
BuildRequires: libimobiledevice-devel
BuildRequires: gtk-doc
%if %{_with_systemd}
BuildRequires: systemd-units >= 37
Requires(post): systemd-units
Requires(post): systemd-sysvinit
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif
Requires: pm-utils
Obsoletes: devicekit-power

%description
%{oname} provides a daemon, API and command line tools for
managing power devices attached to the system.

%package -n %libname
Summary: Shared Library of %{oname}
Group: System/Libraries
Requires: %name >= %version-%release
Obsoletes: %oldlibname

%description -n %libname
%{oname} provides a daemon, API and command line tools for
managing power devices attached to the system.


%package -n %develname
Summary: Headers and libraries for %{oname}
Group: Development/C
Provides: %{oname}-devel = %{version}-%{release}
Requires: %{name} = %{version}
Requires: %libname = %version-%release
Obsoletes: %olddevelname

%description -n %develname
Headers and libraries for %{oname}

%prep
%setup -q
%apply_patches

%build
%configure2_5x --disable-dependency-tracking --enable-gtk-doc
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%if %{_with_systemd}
install -m 0644 -D %{SOURCE1} %{buildroot}%{_unitdir}/upowerd.service
sed -i -e 's#/usr/lib#%{_libdir}#g' %{buildroot}%{_unitdir}/upowerd.service
%endif

%find_lang %name

%clean
rm -rf %{buildroot}


%if %{_with_systemd}
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


%files -f %name.lang
%defattr(-,root,root,-)

%doc README AUTHORS NEWS HACKING
%dir %_sysconfdir/UPower/
%config(noreplace) %_sysconfdir/UPower/UPower.conf
%{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules

%{_bindir}/*
%{_libexecdir}/upowerd

%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service
%if %{_with_systemd}
%{_unitdir}/upowerd.service
%endif

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/libupower-glib.so.%{major}*
%{_libdir}/girepository-1.0/UPowerGlib-1.0.typelib

%files -n %develname
%{_datadir}/dbus-1/interfaces/*.xml
%dir %{_datadir}/gtk-doc/html/UPower
%{_datadir}/gtk-doc/html/UPower/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/upower-glib.pc
%{_datadir}/gir-1.0/UPowerGlib-1.0.gir
%{_includedir}/libupower-glib
