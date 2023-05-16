# Project #3 - Train Booking

## Description

This is a collaboration to complete the group project in the **Intro to Database Systems** Course at FCAI-CU.\
Project 3 which is the train booking program is capable of organizing passengers, their accounts, trains, trips and more.

## Proposed or Required Functionalities

- Signing up a new user (e.g. admin, customer)
- Updating a user's details
- Adding a train (by admin)
- Updating a train details (by admin)
- Adding a trip (by admin)
- Updating a trip details (by admin)
- Showing a list of available seats that satisfy certain criteria  
(e.g. date, time, source, destination, required number of seats…)
- Performing operations on trips: Booking and Canceling.

# Instructions

These instructions guide you on how to run the generated script file, take a backup after making edits to the SQL Server database, and restore the backup if needed.

## Prerequisites

- Microsoft SQL Server installed on your machine.
- Access and permissions to create and modify databases on SQL Server.

## Running the Generated Script

> This is done once to create the database on your machine, afterwards just restore the backup (.bak) file and you're good to go!

1. Open SQL Server Management Studio (SSMS) and connect to your SQL Server instance.
2. Create a new query window by clicking **New Query**.
3. Open the generated script file in a text editor or SQL Server Management Studio.
4. Copy the entire content of the script file.
5. In the query window, paste the copied script.
6. Modify the script if needed (e.g., change database names or paths).
7. Execute the script by clicking **Execute** or pressing **F5**.
8. The script will create or modify the database schema and data based on the provided SQL statements.

## Taking a Database Backup

After completing the edits to the database, it is recommended to take a backup as a precautionary measure.

1. Open SQL Server Management Studio (SSMS) and connect to your SQL Server instance.
2. Right-click on the database you want to back up and select **Tasks** > **Back Up**.
3. In the **Back Up Database** wizard, specify the backup destination by selecting **Disk**.
4. Choose the location to save the backup file by clicking the **Add** button.
5. Specify a unique file name for the backup file (e.g., MyDatabaseBackup.bak).
6. Review the backup options and adjust as needed (e.g., compression, backup type).
7. Click **OK** to start the backup process.
8. Once the backup is completed, you will have a backup file that can be used to restore the database if needed.

## Restoring a Database from Backup

If you need to restore the database from the backup file:

1. Open SQL Server Management Studio (SSMS) and connect to your SQL Server instance.
2. Right-click on the **Databases** node and select **Restore Database**.
3. In the **General** tab of the **Restore Database** window, enter a new database name.
4. Select the **Device** option under the **Source** section.
5. Click the **...** button to browse for the backup file.
6. Locate and select the backup file you want to restore.
7. Verify that the **Backup sets to restore** list shows the backup file you selected.
8. Select the appropriate restore options (e.g., leaving the default options is usually sufficient).
9. Click **OK** to start the restore process.
10. Once the restore is completed, the database will be restored to the specified database name.

## Additional Notes

- It is important to ensure that you have appropriate permissions to perform the necessary operations on the SQL Server instance.
- Always review and understand the script content, backup options, and restore options before executing them to avoid unintended consequences.
- Store the backup file in a secure location and consider implementing a regular backup strategy to ensure data protection.

