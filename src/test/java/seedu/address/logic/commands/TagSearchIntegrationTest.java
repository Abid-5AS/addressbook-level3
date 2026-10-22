package seedu.address.logic.commands;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;

import org.junit.jupiter.api.Test;

import seedu.address.logic.parser.AddressBookParser;
import seedu.address.logic.parser.exceptions.ParseException;
import seedu.address.model.AddressBook;
import seedu.address.model.Model;
import seedu.address.model.ModelManager;
import seedu.address.model.UserPrefs;
import seedu.address.model.person.Person;
import seedu.address.testutil.PersonBuilder;

/** Exercises the real command parser, predicates, filtered model and returned count together. */
public class TagSearchIntegrationTest {
    @Test
    public void findTags_matchesWholeTagsIgnoringCaseAndListRestoresAll() throws Exception {
        Person alice = new PersonBuilder().withName("Alice").withTags("friends").build();
        Person bob = new PersonBuilder().withName("Bob").withTags("colleagues").build();
        Person carl = new PersonBuilder().withName("Carl").withTags("friendship").build();
        AddressBook book = new AddressBook();
        book.addPerson(alice);
        book.addPerson(bob);
        book.addPerson(carl);
        Model model = new ModelManager(book, new UserPrefs());
        AddressBookParser parser = new AddressBookParser();
        CommandResult result = parser.parseCommand("find t/FRIENDS colleagues").execute(model);
        assertEquals(List.of(alice, bob), model.getFilteredPersonList());
        assertEquals("2 person(s) listed!", result.getFeedbackToUser());
        parser.parseCommand("find t/friend").execute(model);
        assertEquals(List.of(), model.getFilteredPersonList());
        parser.parseCommand("list").execute(model);
        assertEquals(List.of(alice, bob, carl), model.getFilteredPersonList());
        parser.parseCommand("find Alice").execute(model);
        assertEquals(List.of(alice), model.getFilteredPersonList());
        assertEquals(3, model.getAddressBook().getPersonList().size());
    }

    @Test
    public void findTags_emptyQuery_isRejected() {
        assertThrows(ParseException.class, () -> new AddressBookParser().parseCommand("find t/   "));
    }
}
