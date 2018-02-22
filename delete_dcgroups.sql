-- This will delete all data collection groups and data collections and any other records 
-- where the table has a cascading foreign key pointing to the deleted data collection group records

DELETE FROM DataCollectionGroup WHERE dataCollectionGroupId >= 1054269;
