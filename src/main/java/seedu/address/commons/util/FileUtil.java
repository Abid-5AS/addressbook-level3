package seedu.address.commons.util;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

/**
 * Writes and reads files
 */
public class FileUtil {

    private static final String CHARSET = "UTF-8";

    /**
     * Creates a file if it does not exist along with its missing parent directories.
     * @throws IOException if the file or directory cannot be created.
     */
    public static void createIfMissing(Path file) throws IOException {
        if (Files.exists(file)) {
            return;
        }

        createParentDirsOfFile(file);

        Files.createFile(file);
    }

    /**
     * Creates parent directories of file if it has a parent directory
     */
    private static void createParentDirsOfFile(Path file) throws IOException {
        Path parentDir = file.getParent();

        if (parentDir != null) {
            Files.createDirectories(parentDir);
        }
    }

    /**
     * Assumes file exists
     */
    public static String readFromFile(Path file) throws IOException {
        return new String(Files.readAllBytes(file), CHARSET);
    }

    /**
     * Writes given string to a file.
     * Will create the file if it does not exist yet.
     */
    public static void writeToFile(Path file, String content) throws IOException {
        Files.write(file, content.getBytes(CHARSET));
    }

    /**
     * Replaces a file only after its complete new contents have been written to a sibling temporary file.
     * Fails without a non-atomic fallback if the filesystem does not support atomic replacement.
     */
    public static void writeAtomically(Path file, String content) throws IOException {
        writeAtomically(file, content, FileUtil::writeToFile);
    }

    /** Package-private writer seam allows deterministic interrupted-write regression tests. */
    static void writeAtomically(Path file, String content, ContentWriter writer) throws IOException {
        Path target = file.toAbsolutePath();
        createParentDirsOfFile(target);
        Path temporary = Files.createTempFile(target.getParent(), ".addressbook-", ".tmp");
        try {
            writer.write(temporary, content);
            Files.move(temporary, target, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
        } finally {
            Files.deleteIfExists(temporary);
        }
    }

    /** Writes the staged content; production uses the same UTF-8 writer as ordinary files. */
    @FunctionalInterface
    interface ContentWriter {
        void write(Path file, String content) throws IOException;
    }

}
