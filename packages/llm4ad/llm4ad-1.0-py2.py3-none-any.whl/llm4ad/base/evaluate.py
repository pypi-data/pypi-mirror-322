from __future__ import annotations

import multiprocessing
import sys
import time
from abc import ABC, abstractmethod
from typing import Any

from .code import TextFunctionProgramConverter, Program
from .modify_code import ModifyCode


class Evaluation(ABC):
    def __init__(
            self,
            template_program: str,
            task_description: str = '',
            use_numba_accelerate: bool = False,
            use_protected_div: bool = False,
            protected_div_delta: float = 1e-5,
            random_seed: int | None = None,
            timeout_seconds: int | float = None,
            *,
            exec_code: bool = True,
            safe_evaluate: bool = True,
            daemon_eval_process: bool = False,
            **kwargs
    ):
        """Evaluator for executing generated code.
        Args:
            task_description: a brief description of the algorithm design task and specification.
            template_program: the seed program (in str) as the initial function of the run.
                the template_program should be executable, i.e., incorporating package import, and function definition, and function body.
                The function body can be 'pass' in EoH as EoH does not request the template_program tobe valid.
            use_numba_accelerate: Wrap the function with '@numba.jit(nopython=True)'.
            use_protected_div   : Modify 'a / b' => 'a / (b + delta)'.
            protected_div_delta : Delta value in protected div.
            random_seed         : If is not None, set random seed in the first line of the function body.
            timeout_seconds     : Terminate the evaluation after timeout seconds.
            exec_code           : Using 'exec()' to compile the code and provide the callable function.
                If is set to 'False', the 'callable_func' argument in 'self.evaluate_program' is always 'None'.
                If is set to 'True', the user should provide the score of the program based on 'program_str' argument in 'self.evaluate_program'.
            safe_evaluate       : Evaluate in safe mode using a new process. If is set to False,
                the evaluation will not be terminated after timeout seconds. The user should consider how to
                terminate evaluating in time.
            daemon_eval_process : Set the evaluate process as a daemon process. If set to True,
                you can not set new processes in the evaluator. Which means in self.evaluate_program(),
                you can not create new processes.

        -Assume that: use_numba_accelerate=True, self.use_protected_div=True, and self.random_seed=2024.
        -The original function:
        --------------------------------------------------------------------------------
        import numpy as np

        def f(a, b):
            a = np.random.random()
            return a / b
        --------------------------------------------------------------------------------
        -The modified function will be:
        --------------------------------------------------------------------------------
        import numpy as np
        import numba

        @numba.jit(nopython=True)
        def f():
            np.random.seed(2024)
            a = np.random.random()
            return _protected_div(a, b)

        def _protected_div(a, b, delta=1e-5):
            return a / (b + delta)
        --------------------------------------------------------------------------------
        As shown above, the 'import numba', 'numba.jit()' decorator, and '_protected_dev' will be added by this function.
        """

        self.template_program = template_program
        self.task_description = task_description
        self.use_numba_accelerate = use_numba_accelerate
        self.use_protected_div = use_protected_div
        self.protected_div_delta = protected_div_delta
        self.random_seed = random_seed
        self.timeout_seconds = timeout_seconds
        self.exec_code = exec_code
        self.safe_evaluate = safe_evaluate
        self.daemon_eval_process = daemon_eval_process

    @abstractmethod
    def evaluate_program(self, program_str: str, callable_func: callable) -> Any | None:
        """Evaluate a given function. You can use compiled function (function_callable),
        as well as the original function strings for evaluation.
        Args:
            program_str: The function in string. You can ignore this argument when implementation. (See below).
            callable_func: The callable heuristic function. You can call it using `callable_func(args, kwargs)`.
        Return:
            Returns the fitness value.

        Assume that: self.use_numba_accelerate = True, self.use_protected_div = True,
        and self.random_seed = 2024, the argument 'function_str' will be something like below:
        --------------------------------------------------------------------------------
        import numpy as np
        import numba

        @numba.jit(nopython=True)
        def f(a, b):
            np.random.seed(2024)
            a = a + np.random.random()
            return _protected_div(a, b)

        def _protected_div(a, b, delta=1e-5):
            return a / (b + delta)
        --------------------------------------------------------------------------------
        As shown above, the 'import numba', 'numba.jit()' decorator,
        and '_protected_dev' will be added by this function.
        """
        raise NotImplementedError('Must provide a evaluator for a function.')


class SecureEvaluator:
    def __init__(self, evaluator: Evaluation, debug_mode=False, *, fork_proc: str | bool = 'auto', **kwargs):
        assert fork_proc in [True, False, 'auto', 'default']
        self._evaluator = evaluator
        self._debug_mode = debug_mode

        if self._evaluator.safe_evaluate:
            if fork_proc == 'auto':
                # force MacOS and Linux use 'fork' to generate new process
                if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
                    multiprocessing.set_start_method('fork', force=True)
            elif fork_proc is True:
                multiprocessing.set_start_method('fork', force=True)
            elif fork_proc is False:
                multiprocessing.set_start_method('spawn', force=True)

    def _modify_program_code(self, program_str: str) -> str:
        function_name = TextFunctionProgramConverter.text_to_function(program_str).name
        if self._evaluator.use_numba_accelerate:
            program_str = ModifyCode.add_numba_decorator(
                program_str, function_name=function_name
            )
        if self._evaluator.use_protected_div:
            program_str = ModifyCode.replace_div_with_protected_div(
                program_str, self._evaluator.protected_div_delta, self._evaluator.use_numba_accelerate
            )
        if self._evaluator.random_seed is not None:
            program_str = ModifyCode.add_numpy_random_seed_to_func(
                program_str, function_name, self._evaluator.random_seed
            )
        return program_str

    def evaluate_program(self, program: str | Program):
        try:
            program_str = str(program)
            # record function name BEFORE modifying program code
            function_name = TextFunctionProgramConverter.text_to_function(program_str).name

            program_str = self._modify_program_code(program_str)
            if self._debug_mode:
                print(f'DEBUG: evaluated program:\n{program_str}\n')

            # safe evaluate
            if self._evaluator.safe_evaluate:
                result_queue = multiprocessing.Queue()
                process = multiprocessing.Process(
                    target=self._evaluate_in_safe_process,
                    args=(program_str, function_name, result_queue),
                    daemon=self._evaluator.daemon_eval_process
                )
                process.start()

                if self._evaluator.timeout_seconds is not None:
                    try:
                        # get the result in timeout seconds
                        result = result_queue.get(timeout=self._evaluator.timeout_seconds)
                        # after getting the result, terminate/kill the process
                        process.terminate()
                        process.join()
                    except:
                        # timeout
                        if self._debug_mode:
                            print(f'DEBUG: the evaluation time exceeds {self._evaluator.timeout_seconds}s.')
                        process.terminate()
                        process.join()
                        result = None
                else:
                    result = result_queue.get()
                    process.terminate()
                    process.join()
                return result
            else:
                return self._evaluate(program_str, function_name)
        except Exception as e:
            if self._debug_mode:
                print(e)
            return None

    def evaluate_program_record_time(self, program: str | Program):
        evaluate_start = time.time()
        try:
            program_str = str(program)
            # record function name BEFORE modifying program code
            function_name = TextFunctionProgramConverter.text_to_function(program_str).name

            program_str = self._modify_program_code(program_str)
            if self._debug_mode:
                print(f'DEBUG: evaluated program:\n{program_str}\n')

            # safe evaluate
            if self._evaluator.safe_evaluate:
                result_queue = multiprocessing.Queue()
                process = multiprocessing.Process(
                    target=self._evaluate_in_safe_process,
                    args=(program_str, function_name, result_queue),
                    daemon=self._evaluator.daemon_eval_process
                )
                process.start()

                if self._evaluator.timeout_seconds is not None:
                    try:
                        # get the result in timeout seconds
                        result = result_queue.get(timeout=self._evaluator.timeout_seconds)
                        # after getting the result, terminate/kill the process
                        process.terminate()
                        process.join()
                    except:
                        # timeout
                        if self._debug_mode:
                            print(f'DEBUG: the evaluation time exceeds {self._evaluator.timeout_seconds}s.')
                        process.terminate()
                        process.join()
                        result = None
                else:
                    result = result_queue.get()
                    process.terminate()
                    process.join()
                # return evaluate result and evaluate time
                return result, time.time() - evaluate_start
            else:
                start = time.time()
                score = self._evaluate(program_str, function_name)
                return score, time.time() - start
        except Exception as e:
            if self._debug_mode:
                print(e)
            # return None and evaluate time
            return None, time.time() - evaluate_start

    def _evaluate_in_safe_process(self, program_str: str, function_name, result_queue: multiprocessing.Queue):
        try:
            if self._evaluator.exec_code:
                # compile the program, and maps the global func/var/class name to its address
                all_globals_namespace = {}
                # execute the program, map func/var/class to global namespace
                exec(program_str, all_globals_namespace)
                # get the pointer of 'function_to_run'
                program_callable = all_globals_namespace[function_name]
            else:
                program_callable = None

            # get evaluate result
            res = self._evaluator.evaluate_program(program_str, program_callable)
            result_queue.put(res)
        except Exception as e:
            if self._debug_mode:
                print(e)
            result_queue.put(None)

    def _evaluate(self, program_str: str, function_name):
        try:
            if self._evaluator.exec_code:
                # compile the program, and maps the global func/var/class name to its address
                all_globals_namespace = {}
                # execute the program, map func/var/class to global namespace
                exec(program_str, all_globals_namespace)
                # get the pointer of 'function_to_run'
                program_callable = all_globals_namespace[function_name]
            else:
                program_callable = None

            # get evaluate result
            res = self._evaluator.evaluate_program(program_str, program_callable)
            return res
        except Exception as e:
            if self._debug_mode:
                print(e)
            return None
