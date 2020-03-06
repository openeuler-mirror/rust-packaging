%{?python_enable_dependency_generator}
# https://pagure.io/koji/issue/659
%global debug_package %{nil}

Name:           rust-packaging
Version:        10
Release:        1
Summary:        RPM macros for building Rust packages on various architectures
License:        MIT
URL:            https://pagure.io/fedora-rust/rust2rpm
Source:         https://releases.pagure.org/fedora-rust/rust2rpm/rust2rpm-%{version}.tar.xz

Patch0001:      0001-macros-Do-not-use-awk-s-inplace-feature.patch

BuildRequires:  python3-devel python3-setuptools
# use for check
BuildRequires:  python3-pytest cargo python3-semantic_version

# gawk is needed for stripping dev-deps in macro
Requires:       gawk python3-rust2rpm = %{version}-%{release}
Requires:       rust-srpm-macros = %{version} rust cargo

%description
The package provides macros for building projects in Rust
on various architectures.

%package     -n python3-rust2rpm
Summary:        Convert Rust packages to RPM

Requires:       cargo

Provides:       rust2rpm = %{version}-%{release}
%{?python_provide:%python_provide python3-rust2rpm}

%description -n python3-rust2rpm
Convert Rust packages to RPM.

%prep
%autosetup -n rust2rpm-%{version} -p1

%build
%py3_build

%install
%py3_install
install -D -p -m 0644 -t %{buildroot}%{_rpmmacrodir} data/macros.rust data/macros.cargo
install -D -p -m 0644 -t %{buildroot}%{_fileattrsdir} data/cargo.attr

%check
py.test-%{python3_version} -vv test.py

%files
%defattr(-,root,root)
%license LICENSE
%{_rpmmacrodir}/macros.rust
%{_rpmmacrodir}/macros.cargo
%{_fileattrsdir}/cargo.attr

%files -n python3-rust2rpm
%defattr(-,root,root)
%license LICENSE
%{_bindir}/rust2rpm
%{_bindir}/cargo-inspector
%{python3_sitelib}/rust2rpm/
%{python3_sitelib}/rust2rpm-*.egg-info/

%changelog
* Wed Mar 4 2020 hexiujun <hexiujun1@huawei.com> - 10-1
- Package init
