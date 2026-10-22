package seedu.address.commons.util;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

public class AtomicFileWriteTest {
    @TempDir
    private Path directory;

    @Test
    public void writeAtomically_replacesExistingContentAndCleansStagingFile() throws IOException {
        Path target = directory.resolve("contacts.json");
        Files.writeString(target, "old contents");
        FileUtil.writeAtomically(target, "new contents");
        assertEquals("new contents", Files.readString(target));
        try (var files = Files.list(directory)) {
            assertEquals(1, files.count());
        }
    }

    @Test
    public void writeAtomically_interruptedStaging_preservesOriginalAndCleansTemporary() throws IOException {
        Path target = directory.resolve("contacts.json");
        Files.writeString(target, "original intact");
        assertThrows(IOException.class, () -> FileUtil.writeAtomically(target, "replacement", (temporary, content) -> {
            Files.writeString(temporary, "partial");
            throw new IOException("Simulated disk write interruption");
        }));
        assertEquals("original intact", Files.readString(target));
        try (var files = Files.list(directory)) {
            assertEquals(1, files.count());
        }
    }

    @Test
    public void writeAtomically_createsNestedParentAndPreservesUtf8() throws IOException {
        Path target = directory.resolve("nested/contacts.json");
        FileUtil.writeAtomically(target, "ঢাকা");
        assertEquals("ঢাকা", Files.readString(target));
    }
}
