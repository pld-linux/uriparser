#
# Conditional build
%bcond_without  tests	# disable 'make check'
#
Summary:	A strictly RFC 3986 compliant URI parsing library
Summary(pl.UTF-8):	Biblioteka analizująca URI ściśle zgodne z RFC 3986
Name:		uriparser
Version:	0.7.5
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/uriparser/%{name}-%{version}.tar.lzma
# Source0-md5:	a87b79caa1258cf9f232b55fce66ff22
URL:		http://uriparser.sourceforge.net/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10.1
%{?with_tests:BuildRequires:	cpptest-devel >= 1.1.0}
BuildRequires:	doxygen
BuildRequires:	graphviz-devel
BuildRequires:	libtool
BuildRequires:	lzma >= 1:4.42
BuildRequires:	pkgconfig >= 0.9.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
uriparser is a strictly RFC 3986 compliant URI parsing library.
uriparser is cross-platform, fast, supports Unicode.

%description -l pl.UTF-8
uriparser to biblioteka analizująca URI ściśle zgodne z RFC 3986.
Jest wieloplatformowa, szybka i obsługuje Unicode.

%package devel
Summary:	Header files for uriparser
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki uriparser
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for uriparser.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki uriparser.

%package static
Summary:	Static uriparser library
Summary(pl.UTF-8):	Statyczna biblioteka uriparser
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static uriparser library.

%description static -l pl.UTF-8
Statyczna biblioteka uriparser.

%prep
%setup -q -c -T
lzma -dc %{SOURCE0} | tar xf - -C ..

%build
# configure first in doc, in order to create regular Doxyfile
cd doc
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure
cd ..
%{__libtoolize}
%{__aclocal}
%{__automake}
#%%{__autoheader}
%{__autoconf}
%configure \
	 %{!?with_tests:--disable-test}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog doc/{*.{htm,txt},html}
%attr(755,root,root) %{_libdir}/liburiparser.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liburiparser.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liburiparser.so
%{_libdir}/liburiparser.la
%{_includedir}/uriparser
%{_pkgconfigdir}/liburiparser.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liburiparser.a
