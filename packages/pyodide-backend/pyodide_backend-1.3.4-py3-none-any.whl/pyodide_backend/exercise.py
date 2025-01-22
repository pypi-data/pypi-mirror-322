import json

from .process import WasmProcess, FILENAME
from .task import TaskNoOutput, TaskCaptureCodeExecutionOutput
from pythonwhat import test_exercise


class PyodideExercise:
    def __init__(self, pec: str, solution: str, sct: str):
        self.pec = pec
        self.solution = solution
        self.sct = sct
        self.has_processed_solution = False

        self.user_process = None
        self.submit_process = None
        self.solution_process = None

    def run_init(self):
        self.user_process = WasmProcess()
        self.submit_process = WasmProcess()
        self.solution_process = WasmProcess()

        self.submit_process.shell.displayhook.returns_result = False

        result, _raw_output = self.user_process.executeTask(
            TaskCaptureCodeExecutionOutput([self.pec])
        )

        return result

    def run_code(self, code: str):
        output, _ = self.user_process.executeTask(
            TaskCaptureCodeExecutionOutput([code])
        )
        return str(json.dumps(output))

    def map_output(self, output):
        if output["type"] == "error":
            return {"payload": output["payload"], "type": "error"}

        return {
            "payload": {
                "output": output["payload"],
                "script_name": FILENAME,
            },
            "type": "script-output",
        }

    def run_submit(self, code: str):
        self.submit_process.reset()

        outputs, raw_output = self.submit_process.executeTask(
            TaskCaptureCodeExecutionOutput([self.pec, code])
        )

        if self.has_processed_solution == False:
            self.solution_process.executeTask(TaskNoOutput([self.pec, self.solution]))
            self.has_processed_solution = True

        test_result = test_exercise(
            sct=self.sct,
            student_code=code,
            solution_code=self.solution,
            pre_exercise_code=self.pec,
            student_process=self.submit_process,
            solution_process=self.solution_process,
            raw_student_output=raw_output,
            ex_type="CodingExercise",
            error=None,  # TODO verify if this is ever non-None for coding exercises
        )

        result = [self.map_output(output) for output in outputs] + [
            {"payload": test_result, "type": "sct"},
        ]

        return str(json.dumps(result))
