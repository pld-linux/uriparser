#
# Conditional build
%bcond_without  doc		# generated documentation
%bcond_without  static_libs	# static library
%bcond_without  tests		# unit tests
#
Summary:	A strictly RFC 3986 compliant URI parsing library
Summary(pl.UTF-8):	Biblioteka analizująca URI ściśle zgodne z RFC 3986
Name:		uriparser
Version:	0.9.8
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/uriparser/uriparser/releases
Source0:	https://github.com/uriparser/uriparser/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	64b8b3fead359b4bfb6aab8c307016ad
Patch0:		%{name}-doxygen.patch
URL:		https://uriparser.github.io/
BuildRequires:	cmake >= 3.5.0
%{?with_tests:BuildRequires:	gtest-devel >= 1.8.1-3}
%if %{with doc}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
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

%package apidocs
Summary:	API documentation for uriparser library
Summary(pl.UTF-8):	Dokumentacja API biblioteki uriparser
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for uriparser library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki uriparser.

%prep
%setup -q
%patch0 -p1

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DURIPARSER_BUILD_DOCS=OFF \
	-DURIPARSER_BUILD_TESTS=OFF \
	-DURIPARSER_BUILD_TOOLS=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	%{!?with_doc:-DURIPARSER_BUILD_DOCS=OFF} \
	%{!?with_tests:-DURIPARSER_BUILD_TESTS=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT

# make export files directory clean before shared lib install
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with doc}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/html
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog GOALS.txt README.md THANKS TODO.txt
%attr(755,root,root) %{_bindir}/uriparse
%attr(755,root,root) %{_libdir}/liburiparser.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liburiparser.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liburiparser.so
%{_includedir}/uriparser
%{_libdir}/cmake/uriparser-%{version}
%{_pkgconfigdir}/liburiparser.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liburiparser.a
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/{search,*.css,*.html,*.js,*.png}
%endif
