%if %mdkversion <= 200600
%define    py_platsitedir %{_libdir}/python2.4/site-packages
%endif
%define    name istanbul
%define    version 0.2.2
%define    release %mkrel 2
%define    summary  Desktop Session Recorder

Summary:   %summary
Name:      %name
Version:   %version 
Release:   %release
License:   GPL
Group:     Video
URL:       http://live.gnome.org/Istanbul 
Source:    http://zaheer.merali.org/istanbul-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:  pygtk2.0 pygtk2.0-libglade
Requires: python-xlib
Requires: gnome-python-extras
Requires: gnome-python-gconf
# when suggest tag is implemented, we can change this one

Requires: gstreamer0.10-plugins-base
Requires: gstreamer0.10-plugins-good
Requires: gstreamer0.10-python
BuildRequires: python
BuildRequires: pygtk2.0-libglade
BuildRequires: desktop-file-utils
BuildRequires: pygtk2.0-devel
BuildRequires: gnome-python-extras
BuildRequires: gstreamer0.10-plugins-good
BuildRequires: gstreamer0.10-python-devel
BuildRequires: libgstreamer-plugins-base-devel
BuildRequires: ImageMagick
BuildRequires: automake1.8 intltool libGConf2-devel
BuildRequires: desktop-file-utils
BuildRequires: python-xlib gnome-python-gconf

%description
Istanbul is a desktop session recorder.  You can use it to record your desktop 
session and then play it back for demos, tutorials and presentations.  Sessions 
are recorded to ogg theora files for later playback.

%prep
%setup -q

%build
%configure2_5x
%make 

%install
rm -rf %buildroot
%makeinstall
%if %_lib != lib
mkdir -p %buildroot%_libdir
mv %buildroot%_prefix/lib/python* %buildroot%_libdir
%endif
rm -f %buildroot%{py_platsitedir}/istanbul/extern/pytrayicon/*.la

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="Video;Recorder" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


for i in 16 32 48; do 
    convert %buildroot/%{_datadir}/pixmaps/%{name}.png -size ${i}x${i} %{name}-${i}.png
done

install -m0644 %{name}-16.png -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m0644 %{name}-32.png -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m0644 %{name}-48.png -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%find_lang %name
rm -f %buildroot%_libdir/gstreamer-0.10/libistximagesrc.*a

%clean
rm -rf %buildroot


%files  -f %name.lang
%defattr(-,root,root,-)
%doc ChangeLog 
#NEWS README AUTHORS
%_sysconfdir/gconf/schemas/%name.schemas
%_mandir/man1/%name.1*
%{_bindir}/%{name}
%{py_platsitedir}/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%_libdir/gstreamer-0.10/libistximagesrc.so*
%{_miconsdir}/%{name}.png 
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%post
%{update_menus}
%post_install_gconf_schemas %name

%preun
%preun_uninstall_gconf_schemas %name

%postun
%{clean_menus}


