Below is a **complete “enhanced prompt”** you can give to a generative‑AI (ChatGPT, Claude, Gemini, etc.) so that it will **produce a ready‑to‑run prototype of a multi‑language fuzzing harness for the DataJourney project on Replit, using the ⚡ *Bolt* CLI** to bootstrap the environment.

---

## 🎯 Goal
Create a **single‑repo Replit project** that

1. Installs and configures the fuzzers listed in the original brief (AFL, Radamsa, Jazzer, pytest‑fuzz, go‑fuzz).
2. Provides **minimal, working example targets** for each language (Python, JavaScript/Node, Java, Go).
3. Supplies **scripts** that run the fuzzers locally and in CI.
4. Generates **HTML/JSON reports** that can be opened from the Replit preview pane.
5. Uses **Bolt** (`replit pull` / `replit push`‑style project definition) so the whole workspace can be launched with a single `bolt run` on any Replit (or locally via Docker).

---

## 📂 Repository Layout (what the AI should create)

```
/.replit                 ← Replit entrypoint (run command, language)
bolt.yaml                ← Bolt definition (install, start, test)
.nix/                    ← Optional Nix packages (if needed)
Dockerfile               ← Fallback Docker image (used by Bolt)
requirements.txt        ← Python deps
package.json             ← Node deps
pom.xml                  ← Maven (Jazzer) – Java deps
go.mod / go.sum          ← Go module
src/
 ├─ python/
 │   ├─ target.py        ← tiny vulnerable function (e.g., int div)
 │   └─ test_fuzz.py    ← pytest‑fuzz harness
 ├─ javascript/
 │   ├─ target.js        ← simple parser that can crash on bad JSON
 │   └─ fuzz.js          ← Radamsa‑driven fuzzer script
 ├─ java/
 │   └─ com/example/
 │       └─ Vulnerable.java   ← class with a native‑array‑out‑of‑bounds bug
 └─ go/
     └─ fuzz/
         └─ vuln.go         ← function with a panic on malformed input
scripts/
 ├─ run_afl.sh          ← compile & launch AFL on the C shim of Go target
 ├─ run_jazzer.sh       ← wrapper to start Jazzer on the Java class
 ├─ run_py_fuzz.sh      ← invoke pytest‑fuzz
 ├─ run_js_fuzz.sh      ← invoke Radamsa → Node
 └─ run_go_fuzz.sh      ← invoke go‑fuzz
ci/
 └─ .github/
     └─ workflows/
         └─ fuzz.yml    ← GitHub Actions CI that runs all fuzzers
reports/
 └─ (generated at runtime – HTML/JSON)
```

---

## ⚙️ Bolt Specification (`bolt.yaml`)

The AI must emit a **`bolt.yaml`** that tells Bolt how to prepare the environment on Replit:

```yaml
# bolt.yaml – the single source of truth for the Replit workspace
name: datajourney-fuzz
description: >
  Multi‑language fuzzing prototype for DataJourney.
  Includes AFL, Radamsa, Jazzer, pytest‑fuzz, go‑fuzz.
runtime:
  # Use the official Replit base image (Ubuntu) + Nix for extra packages
  image: ghcr.io/replit/replit:latest
install:
  # System packages
  - apt-get update && apt-get install -y \
      build-essential clang llvm clang-tools \
      libglib2.0-dev libpixman-1-dev \
      radamsa \
      openjdk-17-jdk \
      golang-go \
      python3-pip
  # Language‑specific deps
  - pip install -r requirements.txt
  - npm ci
  - mvn -B dependency:resolve   # pulls Jazzer dependencies
  - go mod tidy
start:
  # By default show a small menu in the Replit console
  - echo "📊  Fuzzing demo ready"
  - echo "   • ./scripts/run_afl.sh"
  - echo "   • ./scripts/run_js_fuzz.sh"
  - echo "   • ./scripts/run_py_fuzz.sh"
  - echo "   • ./scripts/run_jazzer.sh"
  - echo "   • ./scripts/run_go_fuzz.sh"
  - echo "   • open ./reports/index.html to view results"
test:
  # Used by `bolt test` – runs the whole suite in CI‑like mode
  - ./scripts/run_py_fuzz.sh --max-time 30
  - ./scripts/run_js_fuzz.sh --iterations 1000
  - ./scripts/run_jazzer.sh --max-total-time 30s
  - ./scripts/run_go_fuzz.sh -runs=10000
```

*If the user prefers a pure Dockerfile, the AI should also emit one that mirrors the install steps above; Bolt will auto‑detect it.*

---

## 🛠️ Fuzzing Harnesses (minimal but functional)

### 1. Python – `pytest-fuzz`

**`src/python/target.py`**

```python
def unsafe_div(a: int, b: int) -> float:
    """Divides a by b – crashes on division‑by‑zero."""
    return a / b          # <-- raises ZeroDivisionError
```

**`src/python/test_fuzz.py`**

```python
import pytest
from hypothesis import given, strategies as st
from target import unsafe_div

# pytest‑fuzz works via hypothesis; we add a simple wrapper.
@given(st.integers(), st.integers(min_value=-1000, max_value=1000))
def test_unsafe_div(a, b):
    try:
        unsafe_div(a, b)
    except ZeroDivisionError:
        # Expected crash – let hypothesis treat it as a failure
        assert b == 0
```

**`scripts/run_py_fuzz.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../src/python"
# install pytest‑fuzz if not already (bolt already did pip install)
pytest -q --maxfail=1 --fuzz
```

### 2. JavaScript/Node – Radamsa

**`src/javascript/target.js`**

```js
// A tiny JSON parser that throws on malformed input
function parse(data) {
  // JSON.parse throws on bad JSON – that's our “crash”
  return JSON.parse(data);
}

module.exports = { parse };
```

**`scripts/run_js_fuzz.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../src/javascript"

# Create a temporary corpus folder if missing
mkdir -p corpus
printf '{"valid":"json"}\n' > corpus/seed.json

# Run Radamsa to mutate the seed and feed to node
for i in $(seq 1 2000); do
  radamsa corpus/seed.json > fuzz_input_$i.json
  node -e "require('./target').parse(require('fs').readFileSync('fuzz_input_$i.json','utf8'))" \
    && rm -f fuzz_input_$i.json \
    || echo "🛑 Crash on iteration $i" >> ../../reports/js_fuzz.log
done

# Produce a tiny HTML report
cat <<EOF > ../../reports/js_report.html
<!doctype html><html><body>
<h2>JavaScript (Radamsa) fuzzing</h2>
<pre>$(cat ../../reports/js_fuzz.log 2>/dev/null || echo "No crashes")</pre>
</body></html>
EOF
```

### 3. Java – Jazzer

**`pom.xml`** (excerpt – the AI should fill the full Maven skeleton)

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>jazzertest</artifactId>
  <version>1.0-SNAPSHOT</version>
  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <jazzer.version>0.16.0</jazzer.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>com.code-intelligence</groupId>
      <artifactId>jazzer-api</artifactId>
      <version>${jazzer.version}</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.11.0</version>
        <configuration>
          <release>17</release>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

**`src/java/com/example/Vulnerable.java`**

```java
package com.example;

public class Vulnerable {
    // Intentional out‑of‑bounds read – crashes under Jazzer
    public static int trigger(byte[] data) {
        // reading past the end throws ArrayIndexOutOfBoundsException
        return data[data.length];   // <-- bug
    }
}
```

**`src/java/FuzzVulnerable.java`** (Jazzer entry point)

```java
package com.example;

import com.code_intelligence.jazzer.api.FuzzedDataProvider;

public class FuzzVulnerable {
    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        // Feed arbitrary bytes to the vulnerable method
        byte[] bytes = data.consumeRemainingAsBytes();
        try {
            Vulnerable.trigger(bytes);
        } catch (Throwable ignored) {
            // Let Jazzer treat any exception as a crash
        }
    }
}
```

**`scripts/run_jazzer.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../src/java"
# Build the jar with Jazzer's instrumentation
mvn -B package
# Locate the produced jar
JAR=$(find target -name "*jar" | head -n1)
# Run Jazzer (the binary is installed via apt-get earlier)
jazzer --cp $JAR --target_class com.example.FuzzVulnerable \
       --max_total_time=30s \
       --reports_dir=../../reports/jazzer
```

### 4. Go – go‑fuzz

**`src/go/fuzz/vuln.go`**

```go
package fuzz

// Crash on malformed UTF‑8 input – panic triggers go‑fuzz
func Parse(data []byte) {
    s := string(data) // conversion panics on invalid UTF‑8
    // Use the string to silence the compiler
    _ = s
}
```

**`src/go/fuzz/fuzz_test.go`**

```go
//go:build gofuzz
package fuzz

import "testing"

func FuzzParse(f *testing.F) {
    f.Add([]byte("valid"))
    f.Fuzz(func(t *testing.T, data []byte) {
        Parse(data)
    })
}
```

**`scripts/run_go_fuzz.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../src/go/fuzz"

# Build the go-fuzz binary (requires go-fuzz build toolchain)
go install github.com/dvyukov/go-fuzz/go-fuzz@latest
go install github.com/dvyukov/go-fuzz/go-fuzz-build@latest

go-fuzz-build
go-fuzz -bin=./fuzz-fuzz.zip -workdir=../../reports/go_fuzz -maxlen=1024 -timeout=30s
```

### 5. AFL – optional C shim for the Go target

Because AFL works at the binary level, the AI can create a small C driver that calls the Go‑compiled shared library. (The driver is optional; if omitted, the prompt can state “AFL demo not included – replace with your own binary”.)

---

## 📊 Reporting

All scripts write simple **HTML files** into `reports/` (e.g., `js_report.html`, `jazzer/index.html`). The AI should also generate a **summary page** (`reports/index.html`) that links to each language’s detailed report.

**`reports/index.html` (template)**

```html
<!doctype html>
<html>
<head><title>DataJourney – Fuzzing Dashboard</title></head>
<body>
<h1>DataJourney Fuzzing Dashboard</h1>
<ul>
  <li><a href="js_report.html">JavaScript / Radamsa</a></li>
  <li><a href="jazzer/index.html">Java / Jazzer</a></li>
  <li><a href="py_report.html">Python / pytest‑fuzz</a></li>
  <li><a href="go_fuzz/report.html">Go / go‑fuzz</a></li>
</ul>
<p>Generated on <script>document.write(new Date().toLocaleString());</script></p>
</body>
</html>
```

---

## 🤖 What to Ask the AI to Emit

Below is the **final prompt** you should give to the generative model. Paste it *verbatim* (or adapt the wording) when you want the prototype.

---

### **Full Prompt to Generate the Prototype**

```
You are an expert DevOps / security engineer.
Create a **complete, runnable Replit project** that implements a **multi‑language fuzzing demo** for the fictitious “DataJourney” application, using the following tools:

- AFL (for a compiled binary – optional – you may provide a tiny C wrapper around a Go function)
- Radamsa (to mutate inputs for a Node.js target)
- Jazzer (coverage‑guided in‑process fuzzer for a Java class)
- pytest‑fuzz (Hypothesis‑based fuzzing for a Python function)
- go‑fuzz (coverage‑guided fuzzer for a Go package)

The project must be **bootstrap‑able with Bolt** on Replit, i.e. contain a `bolt.yaml` (and optionally a Dockerfile) that installs all system‑level and language‑specific dependencies, then runs a *menu* that tells the user how to launch each fuzzer.

Your answer must include **every file** required, with exact paths, and the content of each file fenced as markdown code blocks. Follow the directory layout below:

```
/
├─ .replit
├─ bolt.yaml
├─ Dockerfile          (optional – if you prefer Docker over apt commands)
├─ requirements.txt
├─ package.json
├─ pom.xml
├─ go.mod
├─ src/
│   ├─ python/
│   │   ├─ target.py
│   │   └─ test_fuzz.py
│   ├─ javascript/
│   │   ├─ target.js
│   │   └─ fuzz.js   (optional – you can embed logic in the run script)
│   ├─ java/
│   │   └─ com/example/
│   │       ├─ Vulnerable.java
│   │       └─ FuzzVulnerable.java
│   └─ go/fuzz/
│       ├─ vuln.go
│       └─ fuzz_test.go
├─ scripts/
│   ├─ run_afl.sh          (can be a stub if you skip AFL)
│   ├─ run_js_fuzz.sh
│   ├─ run_py_fuzz.sh
│   ├─ run_jazzer.sh
│   └─ run_go_fuzz.sh
└─ reports/
    └─ index.html   (generated at runtime)
```

**Requirements for each component**

1. **Python** – a function `unsafe_div(a, b)` that raises `ZeroDivisionError`. Write a `pytest‑fuzz` test using Hypothesis that feeds random integers. The script `run_py_fuzz.sh` must invoke `pytest -q --fuzz`.

2. **JavaScript** – a `parse(data)` function that calls `JSON.parse`. `run_js_fuzz.sh` must generate mutated inputs with `radamsa` (seeded from a single valid JSON file) and pipe them to node, logging any crashes to `reports/js_fuzz.log`. Produce a tiny HTML report (`reports/js_report.html`) that lists crashes.

3. **Java** – a class `Vulnerable` with an out‑of‑bounds array read. Provide a Jazzer entry point `FuzzVulnerable` that uses `FuzzedDataProvider`. `run_jazzer.sh` must compile with Maven, then invoke `jazzer` with a 30‑second budget, writing its built‑in HTML report into `reports/jazzer`.

4. **Go** – a package `fuzz` with a function `Parse([]byte)` that panics on invalid UTF‑8. Add a `FuzzParse` test compliant with `go-fuzz`. `run_go_fuzz.sh` must install `go-fuzz` tools, build the fuzz binary, and run it, storing results in `reports/go_fuzz`.

5. **AFL** – optional. If you provide it, write a tiny C wrapper `afl_driver.c` that links against the compiled Go `vuln.so` and calls `Parse`. Provide a `run_afl.sh` that builds with `clang`, then starts AFL in classic mode (`afl-fuzz`). If you decide not to implement AFL, clearly comment in `run_afl.sh` that it is a placeholder.

**Bolt configuration**

- The `bolt.yaml` must contain `install`, `start`, and `test` sections.
- `install` must use `apt-get` (or `apk` if you choose Alpine) to install `clang`, `llvm`, `radamsa`, `openjdk-17-jdk`, `golang`, `python3‑pip`, `nodejs`/`npm`.
- It must also run `pip install -r requirements.txt`, `npm ci`, `mvn -B dependency:resolve`, and `go mod tidy`.
- `start` should simply echo a friendly menu with the commands to run each fuzzer and a link to `reports/index.html`.
- `test` should sequentially invoke each fuzz script with a short timeout (e.g., 30 s) so that `bolt test` acts like a CI run.

**CI integration**

Also provide a **GitHub Actions workflow** (`.github/workflows/fuzz.yml`) that checks out the repo, runs the same install steps, and executes all `scripts/run_*_fuzz.sh` commands, failing if any script exits with a non‑zero status.

**Additional constraints**

- All scripts must be **POSIX‑compatible** Bash (`#!/usr/bin/env bash`) and exit on error (`set -euo pipefail`).
- Keep the code **tiny but compilable** – the goal is to prove the toolchain works, not to find real bugs.
- The README (optional) should contain a short “How to run locally on Replit” section that tells the user to click **Run** (Bolt will execute the start menu) and then copy‑paste any of the commands shown.

**Output format**

For each file, output:

```
<relative_path>
```
```<language-or-plain>
<file content>
```

Do **not** include any explanatory text outside the fenced blocks, except for the high‑level description at the very top of the answer (you may keep a short intro). The user will copy‑paste the markdown into a new GitHub repo or directly into Replit’s “Import from GitHub” wizard.

---

When the AI finishes, you will have a single commit that can be dropped into a fresh Replit workspace, run `bolt run`, and instantly start fuzzing every language component of DataJourney. Happy fuzzing!
