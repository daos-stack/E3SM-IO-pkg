%global with_mpich 1
%if (0%{?rhel} >= 8)
%global with_openmpi 1
%global with_openmpi3 0
%else
%global with_openmpi 0
%global with_openmpi3 1
%endif

%if (0%{?suse_version} >= 1500)
%global module_load() if [ "%{1}" == "openmpi3" ]; then MODULEPATH=/usr/share/modules module load gnu-openmpi; else MODULEPATH=/usr/share/modules module load gnu-%{1}; fi
%else
%global module_load() module load mpi/%{1}-%{_arch}
%endif

%if %{with_mpich}
%global mpi_list mpich
%endif
%if %{with_openmpi}
%global mpi_list %{?mpi_list} openmpi
%endif
%if %{with_openmpi3}
%if 0%{?fedora}
# this would be nice to use but causes issues with linting
# since that is done on Fedora
#{error: openmpi3 doesn't exist on Fedora}
%endif
%global mpi_list %{?mpi_list} openmpi3
%endif

%if (0%{?suse_version} >= 1500)
%global mpi_libdir %{_libdir}/mpi/gcc
%global mpi_lib_ext lib64
%global mpi_includedir %{_libdir}/mpi/gcc
%global mpi_include_ext /include
%else
%global mpi_libdir %{_libdir}
%global mpi_lib_ext lib
%global mpi_includedir %{_includedir}
%global mpi_include_ext -%{_arch}
%endif

%global shortcommit %(c=%{commit};echo ${c:0:7})

Name:		E3SM-IO
Version:	%{commit}
Release:	1%{?commit:.g%{shortcommit}}%{?dist}
Summary:	File utilities designed for scalability and performance

Group:		System Environment/Libraries
License:	BSD
URL:		https://github.com/Parallel-NetCDF/E3SM-IO
Source:		https://github.com/Parallel-NetCDF/E3SM-IO/archive/%{commit}.tar.gz
BuildRoot:	%_topdir/BUILDROOT
%if (0%{?suse_version} >= 1500)
BuildRequires: lua-lmod
%else
BuildRequires: Lmod
%endif
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool


%if (0%{?suse_version} > 0)
%global __debug_package 1
%global _debuginfo_subpackages 1
%debug_package
%endif

%description
A case study of parallel I/O kernel from the E3SM climate simulation model.

%if %{with_openmpi}
%package openmpi
Summary:	A case study of parallel I/O kernel from the E3SM climate simulation model.
BuildRequires: openmpi-devel
BuildRequires: hdf5-openmpi-devel

%description openmpi
A case study of parallel I/O kernel from the E3SM climate simulation model.
%endif

%if %{with_openmpi3}
%package openmpi3
Summary:	A case study of parallel I/O kernel from the E3SM climate simulation model.
BuildRequires: openmpi3-devel
BuildRequires: hdf5-openmpi3-devel

%description openmpi3
A case study of parallel I/O kernel from the E3SM climate simulation model.
%endif

%if %{with_mpich}
%package mpich
Summary:	File utilities designed for scalability and performance
BuildRequires: mpich-devel
BuildRequires: hdf5-mpich-devel

%description mpich
A case study of parallel I/O kernel from the E3SM climate simulation model.
%endif


%prep
%autosetup -p1

%build
export CC=mpicc
export CXX=mpicxx
export CFLAGS="%{optflags} -fPIC -pie"
export CPPFLAGS="%{optflags} -fPIC -pie"
for mpi in %{?mpi_list}; do
	mkdir $mpi
	pushd $mpi
	%module_load $mpi
	autoreconf -i ../
	../configure \
		--with-hdf5=%{mpi_libdir}/$mpi/ \
		--prefix=%{mpi_libdir}/$mpi
	make
	module purge
	popd
done

%install
rm -rf %{buildroot}
for mpi in %{?mpi_list}; do
	%module_load $mpi
	make install
	module purge
done

%if %{with_openmpi}
%files openmpi
%defattr(-,root,root,-)
%{mpi_libdir}/openmpi/bin/*
%endif

%if %{with_openmpi3}
%files openmpi3
%defattr(-,root,root,-)
%{mpi_libdir}/openmpi3/bin/*
%endif

%if %{with_mpich}
%files mpich
%defattr(-,root,root,-)
%{mpi_libdir}/mpich/bin/*
%endif

%changelog
* Wed Oct 01 2025 Dalton A. Bohning <dalton.bohning@hpe.com> - 76a1c2fabd042423493a455ef3ce72577a3848a2-1
- Initial package
