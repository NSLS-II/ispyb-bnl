-- This will delete all DataCollectionGroups and DataCollections and any other records
-- where the table has a cascading foreign key pointing to the deleted DataCollectionGroup records

DELETE FROM DataCollectionGroup WHERE dataCollectionGroupId >= 1054269;
