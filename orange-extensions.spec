%{?_javapackages_macros:%_javapackages_macros}

Summary:	A pluggable jar containing stubs for the Apple Java Extensions
Name:		orange-extensions
Version:	1.3.0
Release:	1
License:	BSD
Group:		Development/Java
URL:		https://ymasory.github.io/OrangeExtensions/
Source0:	https://github.com/ymasory/OrangeExtensions/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://repo1.maven.org/maven2/com/yuvimasory/%{name}/%{version}/%{name}-%{version}.pom
BuildArch:	noarch

BuildRequires:	java-rpmbuild
BuildRequires:	maven-local

Requires:	java-headless
Requires:	jpackage-utils

%description
Apple's official jar of Java extension stubs allows you to compile
projects that use Apple Java Extensions on platforms other than Mac.
Unfortunately, Apple does not keep its stubs jar up to date.

Some features are:
 *  allows you to compile Apple Java Extensions on Windows, Linux,
    and others.
 *  supports new methods like setDockImage() added for Java 5.
 *  supports methods like revealInFinder() added for Java 5 update 6
    and Java 6 update 1.
 *  supports multi-touch gesture methods added for Java 5 update 7
    and Java 6 update 2.
 *  supports the new eawt and exit handling added for Java 5 Update 8
    and Java 6 Update 3.

%files -f .mfiles
%doc README.md
%doc LICENSE

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q -n OrangeExtensions-%{version}

# Delete all pre-built binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Copy the pom.xml file here
cp %{SOURCE1} ./pom.xml

# Bundle
%pom_xpath_replace "pom:project/pom:packaging" "<packaging>bundle</packaging>" .

# Add an OSGi compilant MANIFEST.MF
%pom_add_plugin org.apache.felix:maven-bundle-plugin . "
<extensions>true</extensions>
<configuration>
	<supportedProjectTypes>
		<supportedProjectType>bundle</supportedProjectType>
		<supportedProjectType>jar</supportedProjectType>
	</supportedProjectTypes>
	<instructions>
		<Bundle-Name>\${project.artifactId}</Bundle-Name>
		<Bundle-Version>\${project.version}</Bundle-Version>
	</instructions>
</configuration>
<executions>
	<execution>
		<id>bundle-manifest</id>
		<phase>process-classes</phase>
		<goals>
			<goal>manifest</goal>
		</goals>
	</execution>
</executions>"

# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8 

%install
%mvn_install

