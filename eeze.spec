#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		ecore_ver	1.0.0
%define		svn		%{nil}

Summary:	Library for manipulating devices through udev
Summary(pl.UTF-8):	Biblioteka do operowania urządzeniami korzystająca z udev
Name:		eeze
%define	subver	beta2
Version:	1.0.0
Release:	0.%{subver}.1
License:	LGPL v2.1
Group:		X11/Libraries
Source0:	http://download.enlightenment.org/releases/%{name}-%{version}.%{subver}.tar.bz2
# Source0-md5:	dc7b009216d351ed282664f8ee47631d
URL:		http://enlightenment.org/p.php?p=about/libs/efreet
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
# ecore-file; ecore-desktop for tests
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	libtool
BuildRequires:	udev-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
Requires:	ecore-file >= %{ecore_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eeze is a library for manipulating devices through udev with a simple and fast
api. It interfaces directly with libudev, avoiding such middleman daemons as
udisks/upower or hal, to immediately gather device information the instant it
becomes known to the system.  This can be used to determine such things as:
  * If a cdrom has a disk inserted
  * The temperature of a cpu core
  * The remaining power left in a battery
  * The current power consumption of various parts
  * Monitor in realtime the status of peripheral devices
  
Each of the above examples can be performed by using only a single eeze
function, as one of the primary focuses of the library is to reduce the
complexity of managing devices.

%package devel
Summary:	Eeze header files
Summary(pl.UTF-8):	Pliki nagłówkowe Eeze
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# ecore-file
BuildRequires:	ecore-devel >= %{ecore_ver}

%description devel
Header files for Efreet.

%description devel -l pl.UTF-8
Pliki nagłówkowe Efreet.

%package static
Summary:	Static Efreet library
Summary(pl.UTF-8):	Statyczna biblioteka Efreet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Efreet library.

%description static -l pl.UTF-8
Statyczna biblioteka Efreet.

%prep
%setup -q -n %{name}-%{version}.%{subver}

sed -i -e 's/-g -O0//' src/lib/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# just tests
rm -f $RPM_BUILD_ROOT%{_bindir}/efreet_{alloc,menu_alloc,test,spec_test,cache_test}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/test

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_libdir}/libeeze%{svn}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeeze%{svn}.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeeze.so
%{_libdir}/libeeze.la
%dir %{_includedir}/eeze-1
%{_includedir}/eeze-1/*.h
%{_pkgconfigdir}/eeze.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeeze.a
%endif
