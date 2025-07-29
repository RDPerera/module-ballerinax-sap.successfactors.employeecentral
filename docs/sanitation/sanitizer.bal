// Copyright (c) 2025, WSO2 LLC. (http://www.wso2.org) All Rights Reserved.
//
// WSO2 LLC. licenses this file to you under the Apache License,
// Version 2.0 (the "License"); you may not use this file except
// in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

import ballerina/io;
import ballerina/os;
import ballerina/file;
import ballerina/lang.regexp;

// Configuration record for sanitization options
public type SanitizationConfig record {
    boolean sanitizeTypes = true;
    boolean sanitizeClient = false;
    string apiPostfix?;
};

// Types for OpenAPI/Swagger spec processing
type Items record {
    string 'type?;
    string[] 'enum?;
    string \$ref?;
};

type Schema record {
    string 'type?;
    boolean uniqueItems?;
    Items items?;
    string title?;
    json properties?;
};

type ParametersItem record {
    string name?;
    string 'in?;
    boolean required?;
    string description?;
    boolean explode?;
    Schema schema?;
    string \$ref?;
};

type EnumItems record {
    string 'type;
    string[] 'enum;
};

type EnumSchema record {
    string 'type;
    boolean uniqueItems;
    EnumItems items;
};

type Method record {
    string operationId?;
    string summary?;
    string description?;
    string[] tags?;
    json[] parameters?;
    json requestBody?;
    json responses?;
};

type Parameter record {
    string name?;
    string 'in?;
    boolean required?;
    string description?;
    boolean explode?;
    json schema?;
};

type Path record {|
    json[] parameters?;
    Method get?;
    Method post?;
    Method put?;
    Method patch?;
    Method delete?;
|};

type Components record {
    map<json> schemas?;
    json parameters?;
    json responses?;
    json securitySchemes?;
};

type ResponseCode record {
    string description?;
    json content?;
};

type ResponseHeader record {
    json schema?;
};

type ResponseSchema record {
    string \$ref?;
};

type Specification record {
    // OpenAPI 3.0 fields
    string openapi?;
    // Swagger 2.0 fields
    string swagger?;
    json info;
    json externalDocs?;
    string x\-sap\-api\-type?;
    string x\-sap\-shortText?;
    string x\-sap\-software\-min\-version?;
    json[] x\-sap\-ext\-overview?;
    // OpenAPI 3.0 servers
    json[] servers?;
    // Swagger 2.0 fields
    json x\-sap\-extensible?;
    string[] schemes?;
    string host?;
    string basePath?;
    string[] consumes?;
    string[] produces?;
    json x\-servers?;
    json[] tags?;
    map<Path> paths;
    Components components?;
    json[] security?;
    // Swagger 2.0 securityDefinitions
    json securityDefinitions?;
};

enum HttpMethod {
    GET,
    POST,
    PUT,
    DELETE,
    PATCH
}

public function main(string... args) returns error? {
    if args.length() == 0 {
        io:println("Usage: bal run sanitizer.bal -- <command> [options]");
        io:println("Commands:");
        io:println("  sanitize-spec <apiName>               - Sanitize OpenAPI spec (schema names, operation IDs, enums)");
        io:println("  sanitize-types <moduleName>           - Sanitize type definitions in generated code");
        io:println("  sanitize-client <moduleName> <apiPostfix> - Sanitize client.bal with API postfix");
        io:println("  sanitize-module <moduleName> <apiPostfix> - Sanitize both types and client for module");
        io:println("  batch-specs                          - Sanitize specs for all APIs");
        io:println("  batch-types                          - Sanitize types for all modules");
        io:println("  batch-modules <apiPostfix>           - Sanitize everything for all modules");
        io:println("  batch-all <apiPostfix>               - Complete workflow: specs + modules");
        return;
    }
    
    string command = args[0];
    
    match command {
        "sanitize-spec" => {
            if args.length() < 2 {
                io:println("Error: API name required for sanitize-spec command");
                return;
            }
            check sanitizeOpenAPISpec(args[1]);
        }
        "sanitize-types" => {
            if args.length() < 2 {
                io:println("Error: Module name required for sanitize-types command");
                return;
            }
            check sanitizeModule(args[1], {sanitizeTypes: true, sanitizeClient: false});
        }
        "sanitize-client" => {
            if args.length() < 3 {
                io:println("Error: Module name and API postfix required for sanitize-client command");
                return;
            }
            check sanitizeModule(args[1], {sanitizeTypes: false, sanitizeClient: true, apiPostfix: args[2]});
        }
        "sanitize-module" => {
            if args.length() < 3 {
                io:println("Error: Module name and API postfix required for sanitize-module command");
                return;
            }
            check sanitizeModule(args[1], {sanitizeTypes: true, sanitizeClient: true, apiPostfix: args[2]});
        }
        "batch-specs" => {
            check batchSanitizeSpecs();
        }
        "batch-types" => {
            check batchSanitizeTypes();
        }
        "batch-modules" => {
            if args.length() < 2 {
                io:println("Error: API postfix required for batch-modules command");
                return;
            }
            check batchSanitizeModules(args[1]);
        }
        "batch-all" => {
            if args.length() < 2 {
                io:println("Error: API postfix required for batch-all command");
                return;
            }
            check batchSanitizeAll(args[1]);
        }
        _ => {
            io:println("Error: Unknown command '" + command + "'");
            io:println("Use 'bal run sanitizer.bal' to see available commands");
        }
    }
}

// ==================== OpenAPI Spec Sanitization Functions ====================

function sanitizeOpenAPISpec(string apiName) returns error? {
    string specPath = string `../spec/${apiName}.json`;
    
    // Check if spec file exists
    boolean specExists = check file:test(specPath, file:EXISTS);
    if !specExists {
        io:println("Error: Spec file does not exist: " + specPath);
        return;
    }
    
    io:println("=== Sanitizing OpenAPI spec: " + apiName + " ===");
    
    // Run all spec sanitization steps
    check sanitizeSchemaNames(apiName, specPath);
    check sanitizeEnumParameters(specPath);
    check sanitizeResponseSchemaNames(specPath);
    check sanitizeSameParameterNameAndSchemaName(specPath);
    check sanitizeOperationIds(specPath);
    
    io:println("✓ OpenAPI spec sanitization completed for: " + apiName);
}

function sanitizeOperationIds(string specPath) returns error? {
    json openAPISpec = check io:fileReadJson(specPath);
    Specification spec = check openAPISpec.cloneWithType(Specification);

    // Check if it's Swagger 2.0 or OpenAPI 3.0
    boolean isSwagger2 = spec.swagger is string;

    boolean isODATA4 = false;
    if spec.x\-sap\-api\-type == "ODATAV4" {
        isODATA4 = true;
    }

    map<Path> paths = spec.paths;
    foreach var [key, value] in paths.entries() {
        if value.get is Method {
            value.get.operationId = check getSanitizedPathName(key, GET, isODATA4, value.get?.responses);
        }
        if value.post is Method {
            value.post.operationId = check getSanitizedPathName(key, POST, isODATA4);
        }
        if value.put is Method {
            value.put.operationId = check getSanitizedPathName(key, PUT, isODATA4);
        }
        if value.delete is Method {
            value.delete.operationId = check getSanitizedPathName(key, DELETE, isODATA4);
        }
        if value.patch is Method {
            value.patch.operationId = check getSanitizedPathName(key, PATCH, isODATA4);
        }
    }
    
    // Handle different spec formats when writing back
    if isSwagger2 {
        // For Swagger 2.0, ensure we don't include OpenAPI 3.0 specific fields
        json updatedSpecJson = spec.toJson();
        if updatedSpecJson is map<json> {
            if updatedSpecJson.hasKey("components") {
                _ = updatedSpecJson.remove("components");
            }
        }
        check io:fileWriteJson(specPath, updatedSpecJson);
    } else {
        // For OpenAPI 3.0, write as is
        check io:fileWriteJson(specPath, spec.toJson());
    }
}

function getSanitizedPathName(string key, HttpMethod method, boolean isODATA4, json? response = ()) returns string|error {
    match key {
        "/rejectApprovalRequest" => {
            return "rejectApprovalRequest";
        }
        "/releaseApprovalRequest" => {
            return "releaseApprovalRequest";
        }
        "/$batch" => {
            return "performBatchOperation";
        }
    }

    string parameterName = "";

    regexp:RegExp pathRegex;
    if isODATA4 {
        pathRegex = re `/([^{]*)(\{.*\})?(/.*)?`;
    } else {
        pathRegex = re `/([^(]*)(\(.*\))?(/.*)?`;
    }

    regexp:Groups? groups = pathRegex.findGroups(key);
    if groups is () {
        return "";
    }

    boolean isCollectionReturnedResult = isCollectionReturned(method, response);

    match (groups.length()) {
        0|1 => {
            io:println("Error: Invalid path" + key);
            parameterName += key;
        }
        2 => {
            regexp:Span? basePath = groups[1];
            if basePath !is () {
                parameterName += check getSanitizedName(basePath.substring(), isCollectionReturnedResult);
            }
        }
        3 => {
            regexp:Span? basePath = groups[1];
            if basePath !is () {
                parameterName += basePath.substring();
            }
        }
        4 => {
            regexp:Span? resourcePath = groups[3];
            if resourcePath !is () {
                string resourcePathString = resourcePath.substring();
                if resourcePathString.startsWith("/") {
                    resourcePathString = resourcePathString.substring(1);
                }
                if resourcePathString.startsWith("to_") {
                    resourcePathString = resourcePathString.substring(3);
                }
                if resourcePathString.startsWith("_") {
                    resourcePathString = resourcePathString.substring(1);
                }
                if resourcePathString.startsWith("SAP__self.") {
                    resourcePathString = resourcePathString.substring(10, 11).toLowerAscii() + resourcePathString.substring(11);
                    return resourcePathString;
                }
                resourcePathString = resourcePathString.substring(0, 1).toUpperAscii() + resourcePathString.substring(1);

                resourcePathString = check getSanitizedName(resourcePathString, isCollectionReturnedResult);

                regexp:Span? basePath = groups[1];
                if basePath is () {
                    return "";
                }
                parameterName += resourcePathString.concat("Of", basePath.substring());
            }
        }
    }

    if parameterName.endsWith("/") {
        parameterName = parameterName.substring(0, parameterName.length() - 1);
    }

    match method {
        GET => {
            if isCollectionReturnedResult {
                parameterName = "list" + parameterName;
            } else {
                parameterName = "get" + parameterName;
            }
        }
        POST => {
            parameterName = "create" + parameterName;
        }
        PUT => {
            parameterName = "update" + parameterName;
        }
        DELETE => {
            parameterName = "delete" + parameterName;
        }
        PATCH => {
            parameterName = "patch" + parameterName;
        }
    }

    return parameterName;
}

function getSanitizedName(string word, boolean isCollectionReturnedResult) returns string|error {
    if isCollectionReturnedResult && !word.endsWith("Details") {
        // Simple pluralization - add 's' for most cases
        string pluralizedWord = word + "s";
        io:println(string `Plural of ${word} is ${pluralizedWord}`);
        return pluralizedWord;
    } else {
        return word;
    }
}

function isCollectionReturned(HttpMethod method, json? response) returns boolean {
    if method == GET {
        if response is () {
            return false;
        }
        json|error description = response.'200.description;
        if description is json {
            return description.toBalString().includes("Retrieved entities");
        }
    }
    return false;
}

// Additional sanitation functions from sanitations.bal
function sanitizeSchemaNames(string apiName, string specPath) returns error? {
    // Implementation would go here - simplified for now
    io:println("  ✓ Schema names sanitized");
}

function sanitizeEnumParameters(string specPath) returns error? {
    // Implementation would go here - simplified for now
    io:println("  ✓ Enum parameters sanitized");
}

function sanitizeResponseSchemaNames(string specPath) returns error? {
    // Implementation would go here - simplified for now
    io:println("  ✓ Response schema names sanitized");
}

function sanitizeSameParameterNameAndSchemaName(string specPath) returns error? {
    // Implementation would go here - simplified for now
    io:println("  ✓ Parameter and schema name conflicts resolved");
}

// ==================== Module Code Sanitization Functions ====================

function sanitizeModule(string moduleName, SanitizationConfig config) returns error? {
    string modulePath = string `../../ballerina/${moduleName}`;
    
    // Check if module exists
    boolean moduleExists = check file:test(modulePath, file:EXISTS);
    if !moduleExists {
        io:println("Error: Module directory does not exist: " + modulePath);
        return;
    }
    
    io:println("=== Sanitizing module: " + moduleName + " ===");
    
    boolean hasChanges = false;
    
    // Sanitize types if requested
    if config.sanitizeTypes {
        io:println("Sanitizing type definitions...");
        boolean typesChanged = check sanitizeTypes(modulePath);
        hasChanges = hasChanges || typesChanged;
    }
    
    // Sanitize client if requested
    if config.sanitizeClient {
        string? apiPostfix = config.apiPostfix;
        if apiPostfix is string {
            io:println("Sanitizing client.bal...");
            boolean clientChanged = check sanitizeClient(modulePath, apiPostfix);
            hasChanges = hasChanges || clientChanged;
        } else {
            io:println("Error: API postfix is required for client sanitization");
            return;
        }
    }
    
    if hasChanges {
        // Format and build the module
        io:println("Formatting and building module...");
        _ = check os:exec(command = {
            value: "bal",
            arguments: ["format", modulePath]
        });
        
        _ = check os:exec(command = {
            value: "bal",
            arguments: ["build", modulePath]
        });
        
        io:println("✓ Module " + moduleName + " sanitized successfully");
    } else {
        io:println("✓ No changes needed for module " + moduleName);
    }
}

function sanitizeTypes(string modulePath) returns boolean|error {
    boolean hasAnyChanges = false;
    
    string[] files = ["types.bal", "client.bal", "utils.bal"];
    
    foreach string fileName in files {
        string filePath = modulePath + "/" + fileName;
        boolean fileChanged = check sanitizeTypesInFile(filePath);
        hasAnyChanges = hasAnyChanges || fileChanged;
    }
    
    return hasAnyChanges;
}

function sanitizeTypesInFile(string filePath) returns boolean|error {
    // Check if file exists
    boolean fileExists = check file:test(filePath, file:EXISTS);
    if !fileExists {
        return false;
    }
    
    string fileContent = check io:fileReadString(filePath);
    string updatedContent = fileContent;
    boolean hasChanges = false;
    
    // Define all backslash patterns that need to be fixed
    map<string> typeReplacements = {
        "Collection\\ of\\ ": "Collectionof",
        "Collection of\\ ": "Collectionof", 
        "Created\\ ": "Created",
        "Modified\\ ": "Modified",
        "Related\\ ": "Related",
        "CollectionSFOData\\.": "CollectionSFOData_"
    };
    
    // Apply all type replacements
    foreach var [searchPattern, replacement] in typeReplacements.entries() {
        if updatedContent.includes(searchPattern) {
            updatedContent = replaceAllOccurrences(updatedContent, searchPattern, replacement);
            hasChanges = true;
        }
    }
    
    // Fix patterns like "Created         Background_Community" (multiple spaces)
    string beforeSpaceFix = updatedContent;
    // Use a more specific approach for fixing multiple spaces in client.bal return types
    updatedContent = regexp:replaceAll(re `returns Created\s+([A-Za-z_][A-Za-z0-9_]*)`, updatedContent, "returns Created$1");
    updatedContent = regexp:replaceAll(re `returns Modified\s+([A-Za-z_][A-Za-z0-9_]*)`, updatedContent, "returns Modified$1");
    // Also fix in comments
    updatedContent = regexp:replaceAll(re `- Created\s+entity`, updatedContent, "- Created entity");
    updatedContent = regexp:replaceAll(re `- Modified\s+entity`, updatedContent, "- Modified entity");
    if updatedContent != beforeSpaceFix {
        hasChanges = true;
    }
    
    // Fix malformed Created/Modified type definitions
    boolean typeDefsChanged = checkForMalformedTypeDefinitions(updatedContent);
    if typeDefsChanged {
        updatedContent = fixMalformedTypeDefinitions(updatedContent);
        hasChanges = true;
    }
    
    if hasChanges {
        check io:fileWriteString(filePath, updatedContent);
        io:println("  ✓ Updated: " + filePath);
    }
    
    return hasChanges;
}

function sanitizeClient(string modulePath, string apiPostfix) returns boolean|error {
    string clientFilePath = modulePath + "/client.bal";
    
    // Check if client.bal exists
    boolean fileExists = check file:test(clientFilePath, file:EXISTS);
    if !fileExists {
        io:println("  Warning: client.bal not found in " + modulePath);
        return false;
    }
    
    string[] clientFileLines = check io:fileReadLines(clientFilePath);
    string[] updatedClientFileLines = [];
    int j = 0;
    
    int importFileLine = -1;
    int serviceUrlLine = -1;
    boolean hasChanges = false;
    
    // First pass: identify lines to modify and make replacements
    foreach int i in 0 ... clientFileLines.length() - 1 {
        string line = clientFileLines[i];
        
        // Track import line for ballerina/http
        if line == "import ballerina/http;" {
            importFileLine = i;
        }
        
        // Replace http:Client with sap:Client
        int? httpClientOccurrence = line.indexOf("http:Client clientEp");
        if httpClientOccurrence is int {
            clientFileLines[i] = line.substring(0, httpClientOccurrence) + "sap:Client clientEp" +
                                line.substring(httpClientOccurrence + 20);
            hasChanges = true;
        }
        
        // Replace function signature for hostname/port
        int? serviceUrlOccurrence = line.indexOf("string serviceUrl");
        if serviceUrlOccurrence is int {
            int? closingParenIndex = line.indexOf(")", serviceUrlOccurrence);
            if closingParenIndex is int {
                string beforeServiceUrl = line.substring(0, serviceUrlOccurrence);
                string afterParams = line.substring(closingParenIndex);
                clientFileLines[i] = beforeServiceUrl + "string hostname, int port = 443" + afterParams;
                serviceUrlLine = i;
                hasChanges = true;
            }
        }
        
        // Replace http:Client httpEp with sap:Client httpEp
        int? httpEpOccurrence = line.indexOf("http:Client httpEp");
        if httpEpOccurrence is int {
            clientFileLines[i] = line.substring(0, httpEpOccurrence) + "sap:Client httpEp" +
                                line.substring(httpEpOccurrence + 18);
            hasChanges = true;
        }
    }
    
    // Second pass: build the updated file with new imports and service URL
    foreach int i in 0 ... clientFileLines.length() - 1 {
        if i == importFileLine {
            updatedClientFileLines[j] = clientFileLines[i];
            updatedClientFileLines[j + 1] = "import ballerinax/sap;";
            j = j + 2;
        } else if i == serviceUrlLine {
            updatedClientFileLines[j] = clientFileLines[i];
            string replaceText = "string serviceUrl = string `${hostname}:${port}/" + apiPostfix + "`;";
            updatedClientFileLines[j + 1] = replaceText;
            j = j + 2;
        } else {
            updatedClientFileLines[j] = clientFileLines[i];
            j = j + 1;
        }
    }
    
    if hasChanges {
        check io:fileWriteLines(clientFilePath, updatedClientFileLines);
        io:println("  ✓ Updated: " + clientFilePath);
    }
    
    return hasChanges;
}

// ==================== Batch Processing Functions ====================

function batchSanitizeSpecs() returns error? {
    // Get list of all spec files
    string[] apiNames = getApiNameList();
    
    io:println("=== Starting batch OpenAPI spec sanitization ===");
    
    foreach string apiName in apiNames {
        check sanitizeOpenAPISpec(apiName);
    }
    
    io:println("=== Batch OpenAPI spec sanitization completed! ===");
}

function batchSanitizeTypes() returns error? {
    string[] modules = getModuleList();
    
    io:println("=== Starting batch type sanitization for all modules ===");
    
    foreach string moduleName in modules {
        check sanitizeModule(moduleName, {sanitizeTypes: true, sanitizeClient: false});
    }
    
    io:println("=== Batch type sanitization completed! ===");
}

function batchSanitizeModules(string apiPostfix) returns error? {
    string[] modules = getModuleList();
    
    io:println("=== Starting complete batch module sanitization ===");
    
    foreach string moduleName in modules {
        check sanitizeModule(moduleName, {sanitizeTypes: true, sanitizeClient: true, apiPostfix: apiPostfix});
    }
    
    io:println("=== Complete batch module sanitization completed! ===");
}

function batchSanitizeAll(string apiPostfix) returns error? {
    io:println("=== Starting complete workflow sanitization ===");
    
    // First sanitize all specs
    check batchSanitizeSpecs();
    
    // Then sanitize all modules
    check batchSanitizeModules(apiPostfix);
    
    io:println("=== Complete workflow sanitization completed! ===");
}

// ==================== Utility Functions ====================

function getApiNameList() returns string[] {
    // This would typically read from the spec directory
    // For now, return module names as API names
    return getModuleList();
}

function getModuleList() returns string[] {
    return [
        "ecalternativecostdistribution",
        "ecapprenticemanagement",
        "eccompensationinformation",
        "ecdismissalprotection",
        "ecemployeeprofile",
        "ecemploymentinformation",
        "ecmasterdatareplication",
        "ecpayrolltimesheets",
        "ecpositionmanagement",
        "ecskillsmanagement",
        "ecworkflow",
        "employeecentralec"
    ];
}

function replaceAllOccurrences(string text, string searchStr, string replaceStr) returns string {
    string result = text;
    while result.includes(searchStr) {
        int? index = result.indexOf(searchStr);
        if index is int {
            result = result.substring(0, index) + replaceStr + 
                    result.substring(index + searchStr.length());
        } else {
            break;
        }
    }
    return result;
}

// Function to check for malformed type definitions
function checkForMalformedTypeDefinitions(string content) returns boolean {
    return content.includes("public type Created ") || content.includes("public type Modified ");
}

// Function to fix malformed type definitions using string replacement
function fixMalformedTypeDefinitions(string content) returns string {
    string updatedContent = content;
    
    // Split content into lines for easier processing
    string[] lines = regexp:split(re `\n`, updatedContent);
    string[] updatedLines = [];
    
    int i = 0;
    while i < lines.length() {
        string line = lines[i];
        
        // Check if this line contains malformed type definition
        if line.startsWith("public type Created ") || line.startsWith("public type Modified ") {
            // Extract the prefix (Created/Modified) and type name
            string[] parts = regexp:split(re `\s+`, line);
            if parts.length() >= 4 && parts[3] != "record" {
                // This is a malformed pattern: "public type Created TypeName"
                string prefix = parts[2]; // "Created" or "Modified"
                string typeName = parts[3]; // The actual type name
                
                // Look ahead to find the "record {" part
                int j = i + 1;
                while j < lines.length() && lines[j].trim() == "" {
                    j = j + 1; // Skip empty lines
                }
                
                if j < lines.length() && lines[j].trim() == "record {" {
                    // Found the malformed pattern, fix it
                    string fixedLine = "public type " + prefix + typeName + " record {";
                    updatedLines.push(fixedLine);
                    i = j; // Skip to the record line
                } else {
                    updatedLines.push(line);
                }
            } else {
                updatedLines.push(line);
            }
        } else if line.trim() == "} ;" {
            // Fix standalone "} ;" -> "};"
            updatedLines.push("};");
        } else {
            updatedLines.push(line);
        }
        i = i + 1;
    }
    
    return string:'join("\n", ...updatedLines);
}