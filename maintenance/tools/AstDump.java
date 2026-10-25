import com.sun.source.tree.Tree;
import com.sun.source.util.JavacTask;
import com.sun.source.util.TreeScanner;
import javax.tools.ToolProvider;
import java.util.List;

/** Parses one Java source file using the JDK parser; does not resolve types or create a CPG. */
class AstDump {
    public static void main(String[] args) throws Exception {
        var compiler = ToolProvider.getSystemJavaCompiler();
        try (var files = compiler.getStandardFileManager(null, null, null)) {
            var task = (JavacTask) compiler.getTask(null, files, null, List.of("-proc:none"), null,
                    files.getJavaFileObjects(args[0]));
            for (var unit : task.parse()) {
                new TreeScanner<Void, Integer>() {
                    public Void scan(Tree node, Integer depth) {
                        if (node == null) return null;
                        System.out.println("  ".repeat(depth) + node.getKind());
                        return super.scan(node, depth + 1);
                    }
                }.scan(unit, 0);
            }
        }
    }
}
