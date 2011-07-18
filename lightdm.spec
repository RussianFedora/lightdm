Summary:	Lightweight display manager
Name:		lightdm
Version:	0.4.4
Release:	1%{?dist}.R

URL:		http://people.ubuntu.com/~robert-ancell/lightdm/releases/
License:	GPLv3
Group:		Development/Libraries
Source:		http://people.ubuntu.com/~robert-ancell/lightdm/releases/%{name}-%{version}.tar.gz

BuildRequires:	intltool
BuildRequires:	pam-devel
BuildRequires:	libXdmcp-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libxklavier-devel
BuildRequires:	gtk2-devel
BuildRequires:	vala-devel
BuildRequires:	qt-devel
BuildRequires:	gobject-introspection-devel

Requires:	%{name}-greeter = %{version}-%{release}

%package	gobject
Summary:	Gobject library for LightDM
Group:		User Interface/X

%description    gobject
%{summary} - Gobject API

%package	gobject-devel
Summary:	Gobject library for LightDM
Group:		Development/Libraries
Requires:	%{name}-gobject

%description    gobject-devel
%{summary} - Gtk development library

%package	qt
Summary:	Qt library for LightDM
Group:		User Interface/X

%description    qt
%{summary} - Qt API

%package	qt-devel
Summary:	Qt development library for LightDM
Group:		Development/Libraries
Requires:	%{name}-qt = %{version}-%{release}

%description    qt-devel
%{summary} - development library

%package	gtk-greeter
Summary:	GTK greeter for LightDM
Group:		User Interface/X
Requires:	%{name}-gobject = %{version}-%{release}
Provides:	%{name}-greeter = %{version}-%{release}

%description    gtk-greeter
%{summary} - Gtk greeter

%package	python-gtk-greeter
Summary:	Python-GTK greeter for LightDM
Group:		User Interface/X
Requires:	%{name}-gobject = %{version}-%{release}
Provides:	%{name}-greeter = %{version}-%{release}

%description    python-gtk-greeter
%{summary} - Python-Gtk greeter

%package	vala-gtk-greeter
Summary:	Vala-GTK greeter for LightDM
Group:		User Interface/X
Requires:	%{name}-gobject = %{version}-%{release}
Provides:	%{name}-greeter = %{version}-%{release}

%description    vala-gtk-greeter
%{summary} - Vala-Gtk greeter

%package	qt-greeter
Summary:	Qt greeter for LightDM
Group:		User Interface/X
Requires:	%{name}-qt = %{version}-%{release}
Provides:	%{name}-greeter = %{version}-%{release}

%description    qt-greeter
%{summary} - Qt greeter

%description
LightDM is a lightweight, cross-desktop display manager. Its main features are
a well-defined greeter API allowing multiple GUIs, support for all display
manager use cases, with plugins where appropriate, low code complexity, and
fast performance. Due to its cross-platform nature greeters can be written in
several toolkits, including HTML/CSS/Javascript.

%prep
%setup -q

%build
%configure \
	--prefix=/usr \
	--disable-static \
	--disable-gtk-doc-html \
	--sysconfdir=%{_sysconfdir} \
	--with-dbus-sys=%{_sysconfdir}/dbus-1/system.d \
	--with-log-dir=/var/log/%{name} \
	--with-xauth-dir=/var/run/%{name}/authority
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall DBUS_SYS_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc %{buildroot}/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post gobject -p /sbin/ldconfig
%post qt -p /sbin/ldconfig
%postun	gobject -p /sbin/ldconfig
%postun	qt -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog INSTALL NEWS README
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/init/%{name}.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/*
%{_mandir}/man1/%{name}.*
%{_libdir}/girepository-1.0/LightDM-0.typelib
%{_datadir}/gir-1.0/LightDM-0.gir

%files	gobject
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-gobject*.so.*

%files	gobject-devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-gobject*.so
%{_libdir}/pkgconfig/lib%{name}-gobject*
%{_includedir}/%{name}-gobject*

%files	qt
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-qt*.so.*

%files	qt-devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-qt*.so
%{_libdir}/pkgconfig/lib%{name}-qt*
%{_includedir}/%{name}-qt*

%files  gtk-greeter
%defattr(-,root,root,-)
%{_libexecdir}/lightdm-example-gtk-greeter
%{_datadir}/%{name}/themes/example-gtk-gnome
%{_datadir}/lightdm-example-gtk-greeter/greeter.ui

%files  python-gtk-greeter
%defattr(-,root,root,-)
%{_libexecdir}/lightdm-example-python-gtk-greeter
%{_datadir}/%{name}/themes/example-python-gtk-gnome

%files  vala-gtk-greeter
%defattr(-,root,root,-)
%{_libexecdir}/lightdm-example-vala-gtk-greeter
%{_datadir}/%{name}/themes/example-vala-gtk-gnome
%{_datadir}/vala/vapi/liblightdm-gobject-0.vapi

%files  qt-greeter
%defattr(-,root,root,-)
%{_libexecdir}/lightdm-example-qt-greeter
%{_datadir}/%{name}/themes/example-qt-kde

%changelog
* Mon Jul 18 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.4-1.R
- update to 0.4.4

* Thu May 12 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 0.3.3
- update to 0.3.3
- clean up spec

* Wed Apr 27 2011 Huaren Zhong <huaren.zhong@gmail.com> - 0.3.2
- Rebuild for Fedora

* Fri Jan 14 2011 TI_Eugene <ti.eugene@gmail.com>
- Splitting plugins
