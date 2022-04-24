#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	22.04.0
%define		kframever	5.56.0
%define		qtver		5.15.2
%define		kaname		kopeninghours
Summary:	A library for parsing and evaluating OSM opening hours expressions
Name:		ka5-%{kaname}
Version:	22.04.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	ae73269278c2dafcf5c235f18d2f549a
URL:		https://community.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.2
BuildRequires:	Qt5Network-devel >= 5.15.2
BuildRequires:	Qt5Qml-devel
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 5.44
BuildRequires:	kf5-kholidays-devel >= 5.77
BuildRequires:	kf5-ki18n-devel >= 5.77
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 3.6
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shared-mime-info >= 1.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for parsing and evaluating OSM opening hours expressions.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.


%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKOpeningHours.so.1
%attr(755,root,root) %{_libdir}/libKOpeningHours.so.*.*.*
%dir %{_libdir}/qt5/qml/org/kde/kopeninghours
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/kopeninghours/libkopeninghoursqmlplugin.so
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/kopeninghours/qmldir
%{_datadir}/qlogging-categories5/org_kde_kopeninghours.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KOpeningHours
%{_includedir}/kopeninghours
%{_includedir}/kopeninghours_version.h
%{_libdir}/cmake/KOpeningHours
%{_libdir}/libKOpeningHours.so
