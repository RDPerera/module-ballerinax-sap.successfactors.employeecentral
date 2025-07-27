# Ballerina SAP SuccessFactors Employee Central - Employment Information Connector

## Overview

[SAP SuccessFactors](https://www.sap.com/products/hcm/successfactors.html) is a comprehensive cloud-based human capital management (HCM) solution designed to help organizations manage their workforce effectively.

The `ballerinax/sap.successfactors.employeecentral.ecemploymentinformation` package provides APIs that enable seamless integration with the SAP SuccessFactors Employment Information API. This service allows you to access employment-related information, including job information, employment termination, and work permit data.

## Setup guide

1. Sign in to your SAP SuccessFactors dashboard.

2. Navigate to the `Admin Center` and select `Manage OAuth2 Client Applications`.

3. Create a new OAuth2 client application:
   - Provide a unique application name
   - Set the application URL
   - Configure the required scopes for Employment Information access

4. Note down the following credentials from your OAuth2 application:
   - Client ID
   - Client Secret
   - Company ID
   - Username
   - Password

5. Identify your SuccessFactors API server URL. You can find your company's API server in the [List of API Servers in SAP SuccessFactors](https://help.sap.com/viewer/d599f15995d348a1b45ba5603e2aba9b/LATEST/en-US/af2b8d5437494b12be88fe374eba75b6.html).

## Quickstart

To use the `sap.successfactors.employeecentral.ecemploymentinformation` connector in your Ballerina application, modify the `.bal` file as follows:

### Step 1: Import the module

Import the `sap.successfactors.employeecentral.ecemploymentinformation` module.

```ballerina
import ballerinax/sap.successfactors.employeecentral.ecemploymentinformation as ecemployment;
```

### Step 2: Instantiate a new connector

Use the hostname and credentials to initiate a client.

```ballerina
configurable string hostname = ?;
configurable string username = ?;
configurable string password = ?;
configurable string companyId = ?;

ecemployment:Client ecemploymentClient = check new (
    {
        auth: {
            username,
            password
        }
    },
    hostname
);
```

### Step 3: Invoke the connector operation

Now, utilize the available connector operations.

```ballerina
// Get employee employment information
ecemployment:EmpEmployment[] employmentInfo = check ecemploymentClient->getEmpEmployment("userId123");

// Get employee job information
ecemployment:EmpJob[] jobInfo = check ecemploymentClient->getEmpJob("userId123");

// Get employee work permit information
ecemployment:EmpWorkPermit[] workPermits = check ecemploymentClient->getEmpWorkPermit("userId123");

// Get employment termination information
ecemployment:EmpEmploymentTermination[] terminationInfo = check ecemploymentClient->getEmpEmploymentTermination("userId123");
```

### Step 4: Run the Ballerina application

```bash
bal run
```

## Examples

The SAP SuccessFactors Employee Central Ballerina connectors provide practical examples illustrating usage in various scenarios. Explore these examples, covering use cases like accessing employment information and managing job-related data.

1. **Employment Data Management** - Demonstrates how to retrieve and manage employee employment information, job details, and work permits.

2. **HR Analytics Integration** - Shows how to integrate employment data with analytics platforms for workforce insights and reporting.

3. **Compliance Management** - Illustrates how to track work permits and employment termination data for regulatory compliance.

## API Reference

For detailed API documentation and available operations, refer to the [SAP SuccessFactors Employment Information API documentation](https://help.sap.com/docs/SAP_SUCCESSFACTORS_PLATFORM/d599f15995d348a1b45ba5603e2aba9b/d91ecc323849441cb2773fc86f0eff0f.html).

## Issues and contributions

Issues and Pull Requests are always welcome. Please make sure to read the [contribution guidelines](https://github.com/ballerina-platform/ballerina-lang/blob/master/CONTRIBUTING.md) before starting any work.