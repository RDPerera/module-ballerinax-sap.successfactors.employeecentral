# Ballerina SAP SuccessFactors Employee Central - Workflow Connector

## Overview

[SAP SuccessFactors](https://www.sap.com/products/hcm/successfactors.html) is a comprehensive cloud-based human capital management (HCM) solution designed to help organizations manage their workforce effectively.

The `ballerinax/sap.successfactors.employeecentral.ecworkflow` package provides APIs that enable seamless integration with the SAP SuccessFactors Workflow API. This service allows you to manage workflow processes, approvals, and workflow-related operations for employee transactions.

## Setup guide

1. Sign in to your SAP SuccessFactors dashboard.

2. Navigate to the `Admin Center` and select `Manage OAuth2 Client Applications`.

3. Create a new OAuth2 client application:
   - Provide a unique application name
   - Set the application URL
   - Configure the required scopes for Workflow access

4. Note down the following credentials from your OAuth2 application:
   - Client ID
   - Client Secret
   - Company ID
   - Username
   - Password

5. Identify your SuccessFactors API server URL. You can find your company's API server in the [List of API Servers in SAP SuccessFactors](https://help.sap.com/viewer/d599f15995d348a1b45ba5603e2aba9b/LATEST/en-US/af2b8d5437494b12be88fe374eba75b6.html).

## Quickstart

To use the `sap.successfactors.employeecentral.ecworkflow` connector in your Ballerina application, modify the `.bal` file as follows:

### Step 1: Import the module

Import the `sap.successfactors.employeecentral.ecworkflow` module.

```ballerina
import ballerinax/sap.successfactors.employeecentral.ecworkflow as ecwf;
```

### Step 2: Instantiate a new connector

Use the hostname and credentials to initiate a client.

```ballerina
configurable string hostname = ?;
configurable string username = ?;
configurable string password = ?;
configurable string companyId = ?;

ecwf:Client ecwfClient = check new (
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
// Get workflow requests
ecwf:WfRequest[] wfRequests = check ecwfClient->getWfRequest("requestId123");

// Get pending workflows
ecwf:MyPendingWorkflow[] pendingWorkflows = check ecwfClient->getMyPendingWorkflow("workflowRequestId123");

// Get workflow request steps
ecwf:WfRequestStep[] requestSteps = check ecwfClient->getWfRequestStep("wfRequestId123");
```

### Step 4: Run the Ballerina application

```bash
bal run
```

## Examples

The SAP SuccessFactors Employee Central Ballerina connectors provide practical examples illustrating usage in various scenarios. Explore these examples, covering use cases like workflow automation and approval management.

1. **Workflow Management** - Demonstrates how to retrieve and manage workflow processes and approval chains.

2. **Process Automation** - Shows how to integrate workflow processes with external systems for automated approvals and notifications.

## API Reference

For detailed API documentation and available operations, refer to the [SAP SuccessFactors Workflow API documentation](https://help.sap.com/docs/SAP_SUCCESSFACTORS_PLATFORM/d599f15995d348a1b45ba5603e2aba9b/c508d8543026442d88457f3654b4e91d.html).

## Issues and contributions

Issues and Pull Requests are always welcome. Please make sure to read the [contribution guidelines](https://github.com/ballerina-platform/ballerina-lang/blob/master/CONTRIBUTING.md) before starting any work.
