%bcond_without check
# https://pagure.io/koji/issue/659
%global debug_package %{nil}

Name:           rust-packaging
Version:        21
Release:        1
Summary:        RPM macros for building Rust packages
License:        MIT
URL:            https://pagure.io/fedora-rust/rust2rpm
Source:         https://pagure.io/fedora-rust/rust2rpm/archive/v%{version}/rust2rpm-v%{version}.tar.gz

Patch:            0001-Add-comment-about-unused-macro.patch
Patch:            0002-Allow-easy-overriding-of-the-opt-level-debuginfo-cod.patch
Patch:            0003-Fix-autodetection-of-rpmautospec.patch
Patch:            0004-Print-information-about-written-files.patch

ExclusiveArch:  %{rust_arches}

# gawk is needed for stripping dev-deps in macro
Requires:       gawk python3-rust2rpm = %{version}-%{release}
Requires:       rust-srpm-macros = %{version} rust cargo >= 1.41

%description
The package provides RPM macros for building Rust projects.

Note that rust-srpm-macros is a seperate arch-independent package that
is also required to build Rust packages.

%package     -n python3-rust2rpm
Summary:        Generate RPM spec files for Rust packages
BuildRequires:  python3-devel python3-setuptools

%if %{with check}
BuildRequires:  python3-pytest cargo
%endif

Requires:       cargo
Provides:       rust2rpm = %{version}-%{release}
%{?python_provide:%python_provide python3-rust2rpm}

%description -n python3-rust2rpm
Generate RPM spec files for Rust packages

%prep
%autosetup -n rust2rpm-v%{version} -p1

%build
%py3_build

%install
%py3_install
install -D -p -m 0644 -t %{buildroot}%{_rpmmacrodir} data/macros.rust data/macros.cargo
install -D -p -m 0644 -t %{buildroot}%{_fileattrsdir} data/cargo.attr

%if %{with check}
%check
py.test-%{python3_version} -vv test.py
%endif

%files
%license LICENSE
%{_rpmmacrodir}/macros.rust
%{_rpmmacrodir}/macros.cargo
%{_fileattrsdir}/cargo.attr

%files -n python3-rust2rpm
%license LICENSE
%{_bindir}/rust2rpm
%{_bindir}/cargo-inspector
%{python3_sitelib}/rust2rpm/
%{python3_sitelib}/rust2rpm-*.egg-info/

%changelog
* Sat May 07 2022 jchzhou <jchzhou@outlook.com> - 21-1
- Upgrade to version 21, minor refactor according to upstream

* Tue Jan 18 2022 SimpleUpdate Robot <tc@openeuler.org> - 20-1
- Upgrade to version 20

* Thu Mar 18 2021 shixuantong <shixuantong@huawei.com> - 15-2
- fix install fail issue because nothing provides rust-srpm-macros = 15

* Tue Feb 02 2021 shixuantong <shixuantong@huawei.com> - 15-1
- Upgrade to version 15

* Wed Mar 4 2020 hexiujun <hexiujun1@huawei.com> - 10-1
- Package init
