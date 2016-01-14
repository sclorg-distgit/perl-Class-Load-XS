%{?scl:%scl_package perl-Class-Load-XS}
%{!?scl:%global pkg_name %{name}}

#TODO: BR: Test::Pod::No404s when available
#TODO: BR: Test::Pod::LinkCheck when available

Name:		%{?scl_prefix}perl-Class-Load-XS
Version:	0.06
Release:	5.sc1%{?dist}
Summary:	XS implementation of parts of Class::Load
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/Class-Load-XS/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Class-Load-XS-%{version}.tar.gz
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	%{?scl_prefix}perl(Module::Build)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	%{?scl_prefix}perl(Class::Load) >= 0.20
# ===================================================================
# Regular test suite requirements
# ===================================================================
BuildRequires:	%{?scl_prefix}perl(constant)
BuildRequires:	%{?scl_prefix}perl(Module::Implementation) >= 0.04
BuildRequires:	%{?scl_prefix}perl(Test::Fatal)
BuildRequires:	%{?scl_prefix}perl(Test::More)
BuildRequires:	%{?scl_prefix}perl(Test::Requires)
BuildRequires:	%{?scl_prefix}perl(Test::Without::Module)
BuildRequires:	%{?scl_prefix}perl(version)
# ===================================================================
# Author/Release test requirements
# ===================================================================
%if ! 0%{?scl:1}
BuildRequires:	%{?scl_prefix}perl(Test::CPAN::Changes)
BuildRequires:	%{?scl_prefix}perl(Test::EOL)
BuildRequires:	%{?scl_prefix}perl(Test::NoTabs)
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})

%{?perl_default_filter}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_from_provides /\.so()/d
%filter_setup
%endif

%description
This module provides an XS implementation for portions of Class::Load.
See Class::Load for API details.

%prep
%setup -q -n Class-Load-XS-%{version}

%build
%{?scl:scl enable %{scl} '}
perl Build.PL installdirs=vendor optimize="%{optflags}"
%{?scl:'}
%{?scl:scl enable %{scl} "}
./Build
%{?scl:"}


%install
%{?scl:scl enable %{scl} "}
./Build install destdir=%{buildroot} create_packlist=0
%{?scl:"}
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} - << \EOF}
RELEASE_TESTING=1 ./Build test
%{?scl:EOF}


%files
%doc Changes LICENSE README
%{perl_vendorarch}/auto/Class/
%{perl_vendorarch}/Class/
%{_mandir}/man3/Class::Load::XS.3pm*

%changelog
* Sun Nov 24 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-5
- Rebuilt for SCL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 0.06-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct  8 2012 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06:
  - Require Class::Load 0.20 in the code, not just the distro metadata
    (CPAN RT#80002)
  - Weird classes with either an ISA or VERSION constant would cause the XS to
    blow up badly (CPAN RT#79998)
  - Fixed some broken logic that lead to a segfault from the
    014-weird-constants.t test on some Perls (CPAN RT#80059)
- Bump perl(Class::Load) version requirement to 0.20
- Drop explicit requirement for perl(Class::Load), no longer needed

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.04-2
- Perl 5.16 rebuild

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04:
  - Some small test changes for the latest Module::Implementation and
    Class::Load
- Bump Class::Load version requirement to 0.15
- BR: perl(constant), perl(Module::Implementation) ≥ 0.04, 
  perl(Test::Requires), perl(Test::Without::Module) and perl(version) for test 
  suite

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 0.03-2
- Rebuild for gcc 4.7 in Rawhide

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03:
  - Explicitly include Test::Fatal as a test prerequisite (CPAN RT#72493)

* Wed Nov 16 2011 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize spec for Fedora submission

* Wed Nov 16 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
