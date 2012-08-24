#
# Conditional build
%bcond_without  tests	# disable 'make check'
#
Summary:	A strictly RFC 3986 compliant URI parsing library
Summary(pl.UTF-8):	Biblioteka analizująca URI ściśle zgodne z RFC 3986
Name:		uriparser
Version:	0.7.7
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/uriparser/%{name}-%{version}.tar.bz2
# Source0-md5:	2da950ef006be5a842dcc383cbbeaa78
URL:		http://uriparser.sourceforge.net/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10.1
%{?with_tests:BuildRequires:	cpptest-devel >= 1.1.0}
BuildRequires:	doxygen
BuildRequires:	graphviz-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 0.9.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
uriparser is a strictly RFC 3986 compliant URI parsing library.
uriparser is cross-platform, fast, supports Unicode.

%description -l pl.UTF-8
uriparser to biblioteka analizująca URI ściśle zgodne z RFC 3986. Jest
wieloplatformowa, szybka i obsługuje Unicode.

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
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	 %{!?with_tests:--disable-test}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/uriparser

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
