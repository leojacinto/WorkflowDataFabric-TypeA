// ============================================================================
// SYSLOG TABLE TRUNCATE - Run in Scripts - Background
// ============================================================================
// This deletes ALL syslog records instantly (typically <10 seconds)
// Safe for DemoHub instances - syslog is diagnostic data only
// ============================================================================

(function() {
    var tableName = 'syslog';
    
    gs.info('========================================');
    gs.info('TRUNCATING SYSLOG TABLE');
    gs.info('========================================');
    
    // Get initial count
    var countBefore = new GlideAggregate(tableName);
    countBefore.addAggregate('COUNT');
    countBefore.query();
    var recordsBefore = 0;
    if (countBefore.next()) {
        recordsBefore = parseInt(countBefore.getAggregate('COUNT'));
    }
    
    gs.info('Records before: ' + recordsBefore.toLocaleString());
    
    // TRUNCATE: Delete all records with no WHERE clause
    var startTime = new GlideDateTime();
    var gr = new GlideRecord(tableName);
    gr.query(); // NO conditions = select ALL
    gr.deleteMultiple(); // Delete everything selected
    var endTime = new GlideDateTime();
    
    var duration = endTime.getNumericValue() - startTime.getNumericValue();
    
    // Get final count
    var countAfter = new GlideAggregate(tableName);
    countAfter.addAggregate('COUNT');
    countAfter.query();
    var recordsAfter = 0;
    if (countAfter.next()) {
        recordsAfter = parseInt(countAfter.getAggregate('COUNT'));
    }
    
    var recordsDeleted = recordsBefore - recordsAfter;
    
    gs.info('');
    gs.info('========================================');
    gs.info('TRUNCATE COMPLETE');
    gs.info('========================================');
    gs.info('Records deleted: ' + recordsDeleted.toLocaleString());
    gs.info('Records remaining: ' + recordsAfter.toLocaleString());
    gs.info('Duration: ' + (duration/1000).toFixed(2) + ' seconds');
    gs.info('========================================');
    
    if (recordsAfter === 0) {
        gs.info('✅ SUCCESS: Syslog table is now empty');
        gs.info('💾 Estimated space freed: ~' + Math.round(recordsDeleted * 500 / 1024 / 1024 / 1024) + ' GB');
    } else {
        gs.warn('⚠️  Some records remain - may need to run again');
    }
    
})();

// ============================================================================
// NOTES:
// ============================================================================
// - This is MUCH faster than chunked deletion (instant vs hours)
// - Safe for syslog because it's just diagnostic/troubleshooting data
// - Does NOT impact business processes or user data
// - Table structure remains intact (just empty)
// - New logs will be written normally after truncation
//
// For sys_audit or other tables, use chunked deletion instead as they may
// contain compliance/audit data you want to retain
// ============================================================================
