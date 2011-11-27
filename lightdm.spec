Name:		lightdm
Version:	1.0.6
Release:	1%{?dist}.R
Summary:	A lightweight display manager

Group:		User Interface/X
License:	GPLv3 or LGPLv3
URL:		https://launchpad.net/lightdm
Source0:	http://launchpad.net/lightdm/trunk/%{version}/+download/lightdm-%{version}.tar.gz
Source1:	lightdm-pam
Source2:	lightdm-autologin-pam
Patch0:		lightdm-fix-compile-qt4.patch
Patch1:		lightdm-disable-tests.patch
Patch2:		lightdm-fix-desktop.patch
Patch3:		lightdm-fix-authors.patch
Patch4:		lightdm-fix-rpath.patch

Patch100:	lightdm-1.0.6-theme.patch
Patch101:	lightdm-remove-xauthority-ownership-fix.patch
Patch102:	05_CVE-2011-3153.patch
Patch103:	10_available_languages.patch
Patch104:	11_set_language_in_accountsservice.patch

BuildRequires:	glib2-devel
BuildRequires:	libXdmcp-devel
BuildRequires:	libxcb-devel
BuildRequires:	libxklavier-devel
BuildRequires:	libX11-devel
BuildRequires:	qt-devel
BuildRequires:	gtk3-devel
BuildRequires:	pam-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gettext intltool

Requires(pre):	/usr/sbin/useradd

Requires:	pam
Requires:	/sbin/nologin
Requires:	lightdm-greeter = %{version}-%{release}

Provides:	service(graphical-login) = %{name}

%description
LightDM is a cross-desktop display manager that aims is to be the standard 
display manager for the X.org X server. The motivation for this project is 
there have been many new display managers written since XDM (often based on 
the XDM source). The main difference between these projects is in the GUIs 
(e.g. different toolkits) and performance - this could be better accomplished 
with a common display manager that allows these differences. 

%package	gobject
Summary:	GObject library for LightDM
Group:		User Interface/X
Requires:	%{name} = %{version}-%{release}

%description	gobject
GObject library for LightDM

%package	gobject-devel
Summary:	GObject development library for LightDM
Group:		Development/Libraries
Requires:	%{name}-gobject = %{version}-%{release}
Requires:	pkgconfig

%description	gobject-devel
GObject development library for LightDM

%package	gobject-vala
Summary:	Vala bindings for LightDM
Group:		Development/Libraries
Requires:	%{name}-gobject = %{version}-%{release}

%description	gobject-vala
Vala bindings for LightDM

%package	gobject-doc
Summary:	LightDM Reference Manual
Group:		Documentation

%description	gobject-doc
LightDM Reference Manual

%package	libs
Summary:	GObject Introspection for LightDM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description	libs
GObject Introspection for LightDM

%package	qt
Summary:	Qt library for LightDM
Group:		User Interface/X
Requires:	%{name} = %{version}-%{release}

%description	qt
Qt library for LightDM

%package	qt-devel
Summary:	Qt development library for LightDM
Group:		Development/Libraries
Requires:	%{name}-qt = %{version}-%{release}
Requires:	pkgconfig

%description	qt-devel
Qt development library for LightDM

%package	gtk-greeter
Summary:	GTK Greeter for LightDM
Group:		User Interface/X
Provides:	lightdm-greeter = %{version}-%{release}
Requires:	%{name}-gobject = %{version}-%{release}

%description	gtk-greeter
GTK Greeter for LightDM

%package	qt-greeter
Summary:	Qt Greeter for LightDM
Group:		User Interface/X
Provides:	lightdm-greeter = %{version}-%{release}
Requires:	%{name}-qt = %{version}-%{release}

%description	qt-greeter
Qt Greeter for LightDM

%prep
%setup -q
# force moc rebuild
find ./ -type f -name "*_moc.cpp" -delete
%patch0 -p1 -b .qt4
%patch1 -p1 -b .disable-tests
%patch2 -p1 -b .fix-desktop
%patch3	-p1 -b .fix-authors
%patch4 -p1 -b .fix-rpath

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1


%build
%configure --enable-maintainer-mode \
	--disable-static \
	--enable-liblightdm-qt \
	--enable-gtk-doc-html \
	--with-greeter-theme-dir=%{_datadir}/lightdm/themes \
	--with-greeter-user=lightdm \
	LIBS=-lX11
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
%find_lang %{name}

# Remove static libraries
find $RPM_BUILD_ROOT -type f -name "*.la" -delete
# Remove AppArmor related files
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/apparmor.d/lightdm-guest-session
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/apparmor.d
# Remove init script
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/init/lightdm.conf

# Adding PAM
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/lightdm
cp -f %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/lightdm-autologin

# Creating dirs
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/%{name}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}

%pre
useradd -M -d /var/lib/%{name} -s /sbin/nologin -r %{name} #> /dev/null 2>&1
usermod -d /var/lib/%{name} -s /sbin/nologin %{name} #>/dev/null 2>&1
# ignore errors, as we can't disambiguate between lightdm already existed
# and couldn't create account with the current adduser.
exit 0

%post	gobject -p /sbin/ldconfig

%post	qt -p /sbin/ldconfig

%postun	gobject -p /sbin/ldconfig

%postun	qt -p /sbin/ldconfig

%files -f %{name}.lang
%doc  AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/dm-tool
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%config %{_sysconfdir}/pam.d/lightdm
%config %{_sysconfdir}/pam.d/lightdm-autologin
%{_libexecdir}/%{name}
%{_libexecdir}/%{name}-set-defaults
%{_libexecdir}/%{name}-guest-session-wrapper
%{_datadir}/man/man1/%{name}*
%attr(1777, root, lightdm) %dir %{_localstatedir}/cache/%{name}
%attr(1755, root, lightdm) %dir %{_localstatedir}/log/%{name}

%files	gobject
%{_libdir}/lib%{name}-gobject*.so*

%files	gobject-devel
%{_includedir}/%{name}-gobject*
%{_libdir}/pkgconfig/lib%{name}-gobject*

%files	gobject-vala
%{_datadir}/vala/vapi/lib%{name}-gobject*.vapi

%files	gobject-doc
%{_datadir}/gtk-doc/html/%{name}-gobject*

%files	libs
%{_libdir}/girepository-1.0/LightDM-*.typelib
%{_datadir}/gir-1.0/LightDM-*.gir

%files	qt
%{_libdir}/lib%{name}-qt*.so*

%files	qt-devel
%{_includedir}/%{name}-qt*
%{_libdir}/pkgconfig/lib%{name}-qt*

%files	gtk-greeter
%{_sbindir}/%{name}-gtk-greeter
%{_datadir}/%{name}-gtk-greeter
%{_datadir}/xgreeters/%{name}-gtk-greeter.desktop

%files	qt-greeter
%{_sbindir}/%{name}-qt-greeter
%{_datadir}/xgreeters/%{name}-qt-greeter.desktop

%changelog
* Mon Nov 27 2011 Arkady L. Shane <ashejn@russianfedora.ru> - 1.0.6-1.R
- update to 1.0.6
- fix pam names
- apply some ubuntu patches
- fix Xauthority

* Fri Oct 7 2011 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.1-1
- Initial release
- Added PAM
- Added patch to fix build with qt4
- Added patch to remove tests.
- Added patch to fix .desktop files
- Added patch to fix empty AUTHORS
- Added patch to fix DSO issue

* Sun Jul 31 2011 Alexei Panov <elemc AT atisserv DOT ru> - 0.9.2-1
- update to 0.9.2

* Mon Jul 18 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.4-1.R
- update to 0.4.4
- added patch for QT utils name fedora-qt.patch
- corrected config path in /etc

* Thu May 12 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 0.3.3
- update to 0.3.3
- clean up spec

* Wed Apr 27 2011 Huaren Zhong <huaren.zhong@gmail.com> - 0.3.2
- Rebuild for Fedora

* Fri Jan 14 2011 TI_Eugene <ti.eugene@gmail.com>
- Splitting plugins




