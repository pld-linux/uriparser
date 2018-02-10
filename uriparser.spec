#
# Conditional build
%bcond_without  doc	# disable generated documentation
%bcond_without  tests	# disable 'make check'
#
Summary:	A strictly RFC 3986 compliant URI parsing library
Summary(pl.UTF-8):	Biblioteka analizująca URI ściśle zgodne z RFC 3986
Name:		uriparser
Version:	0.8.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/uriparser/uriparser/releases
Source0:	https://github.com/uriparser/uriparser/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	80c110ec22b70570ec124563a7a63075
Patch0:		%{name}-doxygen.patch
URL:		https://uriparser.github.io/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10.1
%{?with_tests:BuildRequires:	cpptest-devel >= 1.1.0}
%if %{with doc}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig >= 1:0.9.0
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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	 %{!?with_doc:--disable-doc} \
	 %{!?with_tests:--disable-test}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with doc}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/uriparser
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog THANKS
%attr(755,root,root) %{_bindir}/uriparse
%attr(755,root,root) %{_libdir}/liburiparser.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liburiparser.so.1

%files devel
%defattr(644,root,root,755)
%if %{with doc}
%doc doc/html
%endif
%attr(755,root,root) %{_libdir}/liburiparser.so
%{_libdir}/liburiparser.la
%{_includedir}/uriparser
%{_pkgconfigdir}/liburiparser.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liburiparser.a
