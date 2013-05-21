%if %mdkversion <= 200600
%define    py_platsitedir %{_libdir}/python2.4/site-packages
%endif
%define    name istanbul
%define    version 0.2.2
%define    release %mkrel 9
%define    summary  Desktop Session Recorder

Summary:   %summary
Name:      %name
Version:   %version 
Release:   %release
License:   GPL
Group:     Video
URL:       http://live.gnome.org/Istanbul 
Source:    http://zaheer.merali.org/istanbul-%{version}.tar.bz2
Patch: istanbul-fix-recording-with-sound.patch
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
BuildRequires: pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires: imagemagick
BuildRequires: automake1.8 intltool libGConf2-devel
BuildRequires: desktop-file-utils
BuildRequires: python-xlib gnome-python-gconf

%description
Istanbul is a desktop session recorder.  You can use it to record your desktop 
session and then play it back for demos, tutorials and presentations.  Sessions
are recorded to ogg theora files for later playback.

%prep
%setup -q
%patch -p0

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

%if %mdkversion < 200900
%post
%{update_menus}
%post_install_gconf_schemas %name
%endif

%preun
%preun_uninstall_gconf_schemas %name

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif




%changelog
* Mon May 23 2011 Funda Wang <fwang@mandriva.org> 0.2.2-9mdv2011.0
+ Revision: 677818
- rebuild to add gconftool as req

* Wed Nov 03 2010 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.2-8mdv2011.0
+ Revision: 592940
- rebuild for new python 2.7

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.2.2-7mdv2011.0
+ Revision: 437995
- rebuild

* Sun Dec 28 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.2-6mdv2009.1
+ Revision: 320643
- rebuild for new python

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Aug 19 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.2-5mdv2009.0
+ Revision: 273863
- add patch to fix bug #42922

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.2.2-4mdv2009.0
+ Revision: 247313
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Feb 12 2008 Thierry Vignaud <tv@mandriva.org> 0.2.2-2mdv2008.1
+ Revision: 166622
- fix description-line-too-long
- drop old menu
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - fix buildrequires


* Tue Mar 20 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.2-2mdv2007.1
+ Revision: 146952
- update deps

* Tue Feb 27 2007 Michael Scherer <misc@mandriva.org> 0.2.2-1mdv2007.1
+ Revision: 126340
- update to 0.2.2

* Wed Nov 29 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.1-6mdv2007.1
+ Revision: 88365
- fix file list
- unpack patch
- rename patch
- Import istanbul

* Thu Oct 05 2006 Götz Waschk <waschk@mandriva.org> 0.2.1-4mdv2007.0
- fix deps (bug #26309)

* Thu Sep 14 2006 Götz Waschk <waschk@mandriva.org> 0.2.1-3mdv2007.0
- fix a crash

* Wed Aug 30 2006 Götz Waschk <waschk@mandriva.org> 0.2.1-2mdv2007.0
- fix buildrequires

* Sun Jul 30 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.1-1mdv2007.0
- New release 0.2.1

* Mon Jul 17 2006 Götz Waschk <waschk@mandriva.org> 0.2.0-1mdv2007.0
- fix deps
- update file list
- drop patch
- New release 0.2.0

* Tue Jul 11 2006 Götz Waschk <waschk@mandriva.org> 0.1.2-2mdv2007.0
- fix buildrequires

* Mon Jun 19 2006 Götz Waschk <waschk@mandriva.org> 0.1.2-1mdv2007.0
- add xdg menu
- update file list
- drop patch 0
- fix deps
- New release 0.1.2

* Wed Apr 26 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.1-11mdk
- Fix Build for mdv <= 2006.0

* Tue Apr 04 2006 Sebastien Savarin <plouf@mandriva.org> 0.1.1-10mdk
- add missing Requires on gstreamer-vorbis
- use macros
- make specfile "reader friendly"

* Tue Mar 14 2006 Götz Waschk <waschk@mandriva.org> 0.1.1-9mdk
- install in the right dir on x86_64

* Fri Feb 10 2006 Michael Scherer <misc@mandriva.org> 0.1.1-8mdk
- patch 1, stolen from debian, fix the problem regarding icon menu on kde 
- use python macro

* Tue Jan 10 2006 Götz Waschk <waschk@mandriva.org> 0.1.1-7mdk
- fix buildrequires

* Mon Jan 02 2006 Götz Waschk <waschk@mandriva.org> 0.1.1-6mdk
- fix build

* Sat Dec 31 2005 Götz Waschk <waschk@mandriva.org> 0.1.1-5mdk
- depend on the jpeg plugin for the smoke codec

* Fri Sep 30 2005 Götz Waschk <waschk@mandriva.org> 0.1.1-4mdk
- fix buildrequires

* Wed Sep 14 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.1-3mdk
- Fix BuildRequires ( ImageMagick because of convert )

* Tue Jul 05 2005 Michael Scherer <misc@mandriva.org> 0.1.1-2mdk
- fix deps

* Sun Jul 03 2005 Michael Scherer <misc@mandriva.org> 0.1.1-1mdk
- adaptation of spec from John (J5) Palmieri <johnp@redhat.com>
- patch for various bug related to icecast support

