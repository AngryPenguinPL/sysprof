%global major		2
%define libname		%mklibname sysprof %major
%define libnameui	%mklibname sysprof-ui %major
%define devname		%mklibname sysprof -d

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name:		sysprof
Version:	3.30.1
Release:	1
Summary:	A system-wide Linux profiler
Group:		Development/Tools

License:	GPLv3+
URL:		http://www.sysprof.com
Source0:	https://download.gnome.org/sources/sysprof/%{url_ver}/sysprof-%{version}.tar.xz
BuildRequires:	binutils-devel
BuildRequires:	gettext
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	itstool
BuildRequires:	polkit-1-devel
BuildRequires:	pkgconfig(systemd)
BuildRequires:	appstream-util
BuildRequires:	desktop-file-utils
BuildRequires:	libxml2-utils
BuildRequires:	meson

Requires:	hicolor-icon-theme
Requires:	%{name}-cli%{?_isa} = %{version}-%{release}

%description
Sysprof is a sampling CPU profiler for Linux that collects accurate,
high-precision data and provides efficient access to the sampled
calltrees.


%package        cli
Summary:	Sysprof command line utility
Group:		Development/Tools

%description    cli
The %{name}-cli package contains the sysprof-cli command line utility.


%package     -n %libname
Summary:	Sysprof library
Group:		System/Libraries

%description -n %libname
The libsysprof package contains the Sysprof library.


%package     -n %libnameui
Summary:	Sysprof UI library
Group:		System/Libraries

%description -n %libnameui
The libsysprof-ui package contains the Sysprof UI library.


%package        -n %devname
Summary:	Development files for %{name}
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnameui} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{name}-ui-devel = %{version}-%{release}

%description    -n %devname
The %{devname} package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%meson
%meson_build


%install
%meson_install

%find_lang %{name} --with-gnome


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
%meson_test || :


%files
%license COPYING
%doc NEWS README.md TODO AUTHORS
%{_bindir}/sysprof
%{_datadir}/metainfo/org.gnome.Sysprof2.appdata.xml
%{_datadir}/applications/org.gnome.Sysprof2.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.sysprof2.gschema.xml
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mime/packages/sysprof-mime.xml

%files cli -f %{name}.lang
%license COPYING
%{_bindir}/sysprof-cli
%{_libexecdir}/sysprof/sysprofd
%{_datadir}/dbus-1/system.d/org.gnome.Sysprof2.conf
%{_datadir}/dbus-1/system-services/org.gnome.Sysprof2.service
%{_datadir}/polkit-1/actions/org.gnome.sysprof2.policy
%{_unitdir}/sysprof2.service

%files -n %libname
%license COPYING
%{_libdir}/libsysprof-2.so

%files -n %libnameui
%license COPYING
%{_libdir}/libsysprof-ui-2.so

%files -n %devname
%exclude %{_libdir}/libsysprof-capture-2.a
%{_includedir}/sysprof-2/
%{_libdir}/pkgconfig/sysprof-2.pc
%{_libdir}/pkgconfig/sysprof-capture-2.pc
%{_libdir}/pkgconfig/sysprof-ui-2.pc


