# Ballerina SAP SuccessFactors Employee Central Connectors

[![Build](https://github.com/ballerina-platform/module-ballerinax-sap.successfactors.employeecentral/actions/workflows/ci.yml/badge.svg)](https://github.com/ballerina-platform/module-ballerinax-sap.successfactors.employeecentral/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ballerina-platform/module-ballerinax-sap.successfactors.employeecentral/branch/main/graph/badge.svg)](https://codecov.io/gh/ballerina-platform/module-ballerinax-sap.successfactors.employeecentral)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/ballerina-platform/module-ballerinax-sap.successfactors.employeecentral.svg)](https://github.com/ballerina-platform/module-ballerinax-sap.successfactors.employeecentral/commits/main)
[![GitHub Issues](https://img.shields.io/github/issues/ballerina-platform/ballerina-library/module/successfactors.svg?label=Open%20Issues)](https://github.com/ballerina-platform/ballerina-library/labels/module%2Fsuccessfactors)

[SAP SuccessFactors Employee Central](https://www.sap.com/products/hcm/core-hr-payroll.html) is a comprehensive human capital management solution that helps organizations manage their workforce effectively. It provides a unified platform for HR processes including employee data management, organizational structures, and employment lifecycle management.

This repository encompasses all Ballerina packages pertaining to the SAP SuccessFactors Employee Central module. Each package provides seamless integration with specific Employee Central APIs:

## Available Packages

### Core Employee Management

1. The `ballerinax/sap.successfactors.ecemployeeprofile` package provides APIs for managing employee profile information including personal details, education background, and work experience data.

2. The `ballerinax/sap.successfactors.ecemploymentinformation` package enables management of employment-related information including job details, employment status, termination data, and work permits.

3. The `ballerinax/sap.successfactors.employeecentralec` package provides core Employee Central APIs for comprehensive employee data management and organizational structure operations.

### Compensation and Benefits

4. The `ballerinax/sap.successfactors.eccompensationinformation` package handles employee compensation data including salary information, pay scales, and compensation planning.

5. The `ballerinax/sap.successfactors.ecalternativecostdistribution` package manages alternative cost distribution scenarios for employee expenses and cost center allocations.

### Position and Organizational Management

6. The `ballerinax/sap.successfactors.ecpositionmanagement` package provides position management capabilities including position creation, hierarchy management, and organizational structure maintenance.

7. The `ballerinax/sap.successfactors.ecmasterdatareplication` package enables master data replication across Employee Central systems for data consistency and synchronization.

### Time and Payroll

8. The `ballerinax/sap.successfactors.ecpayrolltimesheets` package manages payroll timesheet data including time tracking, attendance records, and payroll processing information.

### Learning and Development

9. The `ballerinax/sap.successfactors.ecskillsmanagement` package handles skills and competency management including skill profiles, competency frameworks, and talent development tracking.

10. The `ballerinax/sap.successfactors.ecapprenticemanagement` package provides apprentice program management capabilities including apprentice registration, progress tracking, and program administration.

### Workflow and Legal

11. The `ballerinax/sap.successfactors.ecworkflow` package manages workflow processes within Employee Central including approval workflows, notifications, and process automation.

12. The `ballerinax/sap.successfactors.ecdismissalprotection` package handles dismissal protection and termination compliance features including legal requirements and documentation.

## Issues and projects

The **Issues** and **Projects** tabs are disabled for this repository as this is part of the Ballerina library. To
report bugs, request new features, start new discussions, view project boards, etc., visit the Ballerina
library [parent repository](https://github.com/ballerina-platform/ballerina-library).

This repository only contains the source code for the package.

## Build from the source

### Prerequisites

1. Download and install Java SE Development Kit (JDK) version 17. You can download it from either of the following
   sources:

    * [Oracle JDK](https://www.oracle.com/java/technologies/downloads/)
    * [OpenJDK](https://adoptium.net/)

   > **Note:** After installation, remember to set the `JAVA_HOME` environment variable to the directory where JDK was
   installed.

2. Download and install [Ballerina Swan Lake](https://ballerina.io/).

3. Download and install [Docker](https://www.docker.com/get-started).

   > **Note**: Ensure that the Docker daemon is running before executing any tests.

### Build options

Execute the commands below to build from the source.

1. To build all packages:

   ```bash
   ./gradlew clean build
   ```

2. To run the tests in all packages:

   ```bash
   ./gradlew clean test
   ```

3. To build the without the tests:

   ```bash
   ./gradlew clean build -x test
   ```

4. To build only one specific package

   ```bash
   ./gradlew clean :ballerina:<module_name>:build
   ```

   | Module Name                    | Connector                                                    |
   |--------------------------------|--------------------------------------------------------------|
   | ecemployeeprofile              | ballerinax/sap.successfactors.ecemployeeprofile             |
   | ecemploymentinformation        | ballerinax/sap.successfactors.ecemploymentinformation       |
   | employeecentralec              | ballerinax/sap.successfactors.employeecentralec             |
   | eccompensationinformation      | ballerinax/sap.successfactors.eccompensationinformation     |
   | ecalternativecostdistribution  | ballerinax/sap.successfactors.ecalternativecostdistribution |
   | ecpositionmanagement           | ballerinax/sap.successfactors.ecpositionmanagement          |
   | ecmasterdatareplication        | ballerinax/sap.successfactors.ecmasterdatareplication       |
   | ecpayrolltimesheets            | ballerinax/sap.successfactors.ecpayrolltimesheets           |
   | ecskillsmanagement             | ballerinax/sap.successfactors.ecskillsmanagement            |
   | ecapprenticemanagement         | ballerinax/sap.successfactors.ecapprenticemanagement        |
   | ecworkflow                     | ballerinax/sap.successfactors.ecworkflow                    |
   | ecdismissalprotection          | ballerinax/sap.successfactors.ecdismissalprotection         |

5. To run tests against different environment:

   ```bash
   isTestOnLiveServer=true ./gradlew clean test 
   ```
   **Note**: `isTestOnLiveServer` is false by default, tests are run against mock server.

6. To debug packages with a remote debugger:

   ```bash
   ./gradlew clean build -Pdebug=<port>
   ```

7. To debug with the Ballerina language:

   ```bash
   ./gradlew clean build -PbalJavaDebug=<port>
   ```

8. Publish the generated artifacts to the local Ballerina Central repository:

    ```bash
    ./gradlew clean build -PpublishToLocalCentral=true
    ```

9. Publish the generated artifacts to the Ballerina Central repository:

   ```bash
   ./gradlew clean build -PpublishToCentral=true
   ```

## Contribute to Ballerina

As an open-source project, Ballerina welcomes contributions from the community.

For more information, go to the [contribution guidelines](https://github.com/ballerina-platform/ballerina-lang/blob/master/CONTRIBUTING.md).

## Code of conduct

All the contributors are encouraged to read the [Ballerina Code of Conduct](https://ballerina.io/code-of-conduct).

## Useful links

* For more information go to the [`sap.successfactors` package](https://lib.ballerina.io/ballerinax/sap.successfactors/latest).
* For example demonstrations of the usage, go to [Ballerina By Examples](https://ballerina.io/learn/by-example/).
* Chat live with us via our [Discord server](https://discord.gg/ballerinalang).
* Post all technical questions on Stack Overflow with the [#ballerina](https://stackoverflow.com/questions/tagged/ballerina) tag.
