## SHUTDOWN RECORD SCHEMA


**Format:** JSON Schema Draft 07  
**Context:** Financial Forensics

JSON

{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "TL Shutdown Evidence Record (Financial)",  
  "type": "object",  
  "required": \[  
    "timestamp\_utc",  
    "trigger\_id",  
    "trigger\_context",  
    "last\_decision\_hash",  
    "signature"  
  \],  
  "properties": {  
    "timestamp\_utc": { "type": "string", "format": "date-time" },  
    "trigger\_id": { "type": "string", "description": "e.g., 'C-003' (Solvency Illusion)" },  
    "trigger\_context": {  
      "type": "object",  
      "properties": {  
        "asset\_id": { "type": "string" },  
        "claimed\_value": { "type": "number" },  
        "missing\_proof": { "type": "string", "description": "The specific Merkle root that failed verification." }  
      }  
    },  
    "last\_decision\_hash": {  
      "type": "string",  
      "description": "SHA-256 of the last valid trade execution. Ensures no trades are 'lost' in the crash."  
    },  
    "signature": {  
      "type": "string",  
      "description": "Ed25519 signature by the System Authority."  
    }  
  }  
}

## ---
