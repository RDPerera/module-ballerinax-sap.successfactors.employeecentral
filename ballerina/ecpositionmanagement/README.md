# Ballerina SAP SuccessFactors Employee Central - Position Management Connector

## Overview

[SAP SuccessFactors](https://www.sap.com/products/hcm/successfactors.html) is a comprehensive cloud-based human capital management (HCM) solution designed to help organizations manage their workforce effectively.

The `ballerinax/sap.successfactors.employeecentral.ecpositionmanagement` package provides APIs that enable seamless integration with the SAP SuccessFactors Position Management API. This service allows you to manage organizational positions, position hierarchies, and position-related information.

## Setup guide

1. Sign in to your SAP SuccessFactors dashboard.

2. Navigate to the `Admin Center` and select `Manage OAuth2 Client Applications`.

3. Create a new OAuth2 client application:
   - Provide a unique application name
   - Set the application URL
   - Configure the required scopes for Position Management access

4. Note down the following credentials from your OAuth2 application:
   - Client ID
   - Client Secret
   - Company ID
   - Username
   - Password

5. Identify your SuccessFactors API server URL. You can find your company's API server in the [List of API Servers in SAP SuccessFactors](https://help.sap.com/viewer/d599f15995d348a1b45ba5603e2aba9b/LATEST/en-US/af2b8d5437494b12be88fe374eba75b6.html).

## Quickstart

To use the `sap.successfactors.employeecentral.ecpositionmanagement` connector in your Ballerina application, modify the `.bal` file as follows:

### Step 1: Import the module

Import the `sap.successfactors.employeecentral.ecpositionmanagement` module.

```ballerina
import ballerinax/sap.successfactors.employeecentral.ecpositionmanagement as ecpos;
```

### Step 2: Instantiate a new connector

Use the hostname and credentials to initiate a client.

```ballerina
configurable string hostname = ?;
configurable string username = ?;
configurable string password = ?;
configurable string companyId = ?;

ecpos:Client ecposClient = check new (
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
// Get position information
ecpos:Position[] positions = check ecposClient->getPosition("positionCode123");

// Get position matrix relationships
ecpos:PositionMatrixRelationship[] matrixRelationships = check ecposClient->getPositionMatrixRelationship("code123");

// Get position requisition status
ecpos:PositionRequisitionStatus[] requisitionStatus = check ecposClient->getPositionRequisitionStatus("code123");
```

### Step 4: Run the Ballerina application

```bash
bal run
```

## Examples

The SAP SuccessFactors Employee Central Ballerina connectors provide practical examples illustrating usage in various scenarios. Explore these examples, covering use cases like organizational structure management and position planning.

1. **Position Management** - Demonstrates how to retrieve and manage organizational positions and hierarchies.

2. **Workforce Planning** - Shows how to manage position requirements and organizational structure for effective workforce planning.

## API Reference

For detailed API documentation and available operations, refer to the [SAP SuccessFactors Position Management API documentation](https://help.sap.com/docs/SAP_SUCCESSFACTORS_PLATFORM/d599f15995d348a1b45ba5603e2aba9b/c508d8543026442d88457f3654b4e91d.html).

## Issues and contributions

Issues and Pull Requests are always welcome. Please make sure to read the [contribution guidelines](https://github.com/ballerina-platform/ballerina-lang/blob/master/CONTRIBUTING.md) before starting any work.
