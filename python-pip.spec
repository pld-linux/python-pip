# TODO
# - can these be removed on linux?
#   site-packages/pip/_vendor/distlib/t32.exe
#   site-packages/pip/_vendor/distlib/t64.exe
#   site-packages/pip/_vendor/distlib/w32.exe
#   site-packages/pip/_vendor/distlib/w64.exe
#
# Conditional build:
%bcond_without	python3_default	# Use Python 3.x for pip executable
%bcond_without	apidocs		# Sphinx documentation
%bcond_with	tests		# test target (not included in sdist)

%define		pypa_docs_theme_ver	d2e63fbfc62af3b7050f619b2f5bb8658985b931

%define		module		pip
%define		pypi_name	pip
Summary:	A tool for installing and managing Python 2 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 2
Name:		python-%{module}
# keep 20.x here for python2 support
Version:	20.3.4
Release:	7
License:	MIT
Group:		Libraries/Python
# Source0Download: https://pypi.python.org/simple/pip/
Source0:	https://pypi.debian.net/pip/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	577a375b66ec109e0ac6a4c4aa99bbd0
URL:		https://pip.pypa.io/
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-scripttest >= 1.3
BuildRequires:	python-virtualenv >= 1.10
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with apidocs}
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx_inline_tabs
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pip is a replacement for easy_install. It uses mostly the same
techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%description -l pl.UTF-8
Pip to zamiennik easy_install. Wykorzystuje w większości te same
techniki do wyszukiwania pakietów, więc pakiety, które dało się
zainstalować przez easy_install, powinny także dać się zainstalować
przy użyciu pipa.

%package -n python3-pip
Summary:	A tool for installing and managing Python 3 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 3
Group:		Libraries/Python
Requires:	python3-setuptools

%description -n python3-pip
Pip is a replacement for easy_install. It uses mostly the same
techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%description -n python3-pip -l pl.UTF-8
Pip to zamiennik easy_install. Wykorzystuje w większości te same
techniki do wyszukiwania pakietów, więc pakiety, które dało się
zainstalować przez easy_install, powinny także dać się zainstalować
przy użyciu pipa.

%package -n pip
Summary:	A tool for installing and managing Python 3 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 3
Group:		Development/Tools
Requires:	python-%{module} = %{version}-%{release}
Conflicts:	python-pip < 7.1.2-3

%description -n pip
Pip is a replacement for easy_install. It uses mostly the same
techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%description -n pip -l pl.UTF-8
Pip to zamiennik easy_install. Wykorzystuje w większości te same
techniki do wyszukiwania pakietów, więc pakiety, które dało się
zainstalować przez easy_install, powinny także dać się zainstalować
przy użyciu pipa.

%package apidocs
Summary:	Documentation for Python pip modules and installer
Summary(pl.UTF-8):	Dokumentacja instalatora i modułów Pythona pip
Group:		Documentation

%description apidocs
Documentation for Python pip modules and installer.

%description apidocs -l pl.UTF-8
Dokumentacja instalatora i modułów Pythona pip.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build %{?with_tests:test}

%if %{with apidocs}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs/html docs/html/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

# RH compatibility
ln -sf pip2 $RPM_BUILD_ROOT%{_bindir}/python-pip

%if %{without python3_default}
ln -sf pip2 $RPM_BUILD_ROOT%{_bindir}/pip
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip2
%attr(755,root,root) %{_bindir}/pip2.*
%attr(755,root,root) %{_bindir}/python-pip
%{py_sitescriptdir}/pip-%{version}-py*.egg-info
%{py_sitescriptdir}/pip

%if %{without python3_default}
%files -n pip
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/_build/html/*
%endif
