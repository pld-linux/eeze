# NOTE: for versions >= 1.8 see efl.spec
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		ecore_ver	1.7.10
%define		eet_ver		1.7.10
%define		eina_ver	1.7.10

Summary:	Library for manipulating devices through udev
Summary(pl.UTF-8):	Biblioteka do operowania urządzeniami korzystająca z udev
Name:		eeze
Version:	1.7.10
Release:	4
License:	BSD
Group:		Libraries
Source0:	http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	dfe17a0870e1430f7459d45e514fbbdd
URL:		http://trac.enlightenment.org/e/wiki/Eeze
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	ecore-con-devel >= %{ecore_ver}
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	ecore-file-devel >= %{ecore_ver}
BuildRequires:	eet-devel >= %{eet_ver}
BuildRequires:	eina-devel >= %{eina_ver}
BuildRequires:	libmount-devel >= 2.18.0
BuildRequires:	libtool
BuildRequires:	udev-devel >= 1:148
BuildRequires:	pkgconfig >= 1:0.22
Requires:	ecore >= %{ecore_ver}
Requires:	eet >= %{eet_ver}
Requires:	eina >= %{eina_ver}
Requires:	libmount >= 2.18.0
Requires:	udev-libs >= 1:148
Obsoletes:	enlightenment-utils-eeze < 1.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eeze is a library for manipulating devices through udev with a simple
and fast API. It interfaces directly with libudev, avoiding such
middleman daemons as udisks/upower or hal, to immediately gather
device information the instant it becomes known to the system. This
can be used to determine such things as:
 - If a CD-ROM has a disk inserted
 - The temperature of a cpu core
 - The remaining power left in a battery
 - The current power consumption of various parts
 - Monitor in realtime the status of peripheral devices.
  
Each of the above examples can be performed by using only a single
eeze function, as one of the primary focuses of the library is to
reduce the complexity of managing devices.

%description -l pl.UTF-8
Eeze to bibliotek do operowania urządzeniami poprzez udev z prostym i
szybkim API. Działa bezpośrednio z libudev, bez pośrednich demonów,
takich jak udisks, upower czy hal, aby zebrać informacje z urządzeń
natychmiast, kiedy staną się znane w systemie. Może to służyć do
określania rzeczy takich jak:
 - włożenie płyty CD
 - termperatura rdzenia procesora
 - pozostała pojemność baterii
 - aktualne zużycie energii przez różne elementy
 - monitorowanie stanu urządzeń peryferyjnych w czasie rzeczywistym.

Każde z tych zapytań może być wykonane przy użyciu jedynie pojedynczej
funkcji eeze, jako że jedną z głównych idei biblioteki jest
ograniczenie skomplikowania zarządzania urządzeniami.

%package devel
Summary:	Eeze header files
Summary(pl.UTF-8):	Pliki nagłówkowe Eeze
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ecore-devel >= %{ecore_ver}
Requires:	eina-devel >= %{eina_ver}
Requires:	udev-devel >= 1:148

%description devel
Header files for Eeze.

%description devel -l pl.UTF-8
Pliki nagłówkowe Eeze.

%package static
Summary:	Static Eeze library
Summary(pl.UTF-8):	Statyczna biblioteka Eeze
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Eeze library.

%description static -l pl.UTF-8
Statyczna biblioteka Eeze.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-eject=/usr/bin/eject \
	--with-mount=/bin/mount \
	--with-umount=/bin/umount
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/eeze_disk_ls
%attr(755,root,root) %{_bindir}/eeze_mount
%attr(755,root,root) %{_bindir}/eeze_scanner
%attr(755,root,root) %{_bindir}/eeze_umount
%attr(755,root,root) %{_libdir}/libeeze.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeeze.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeeze.so
%{_libdir}/libeeze.la
%{_includedir}/eeze-1
%{_pkgconfigdir}/eeze.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeeze.a
%endif
