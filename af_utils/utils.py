from __future__ import absolute_import123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom __future__ import division123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport threading123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport weakref123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom tensorflow.core.protobuf import queue_runner_pb2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom tensorflow.python.framework import errors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom tensorflow.python.framework import ops123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom tensorflow.python.platform import tf_logging as logging123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef var_stats(vals):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "Take a dictionary of variables and variable names, and prints statistics."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    message = ""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    message += "================================================================================\n"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for val in vals:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        message+= ("val:"+str(val))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        message+=(str((vals[val]))+"\n")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for val in vals:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        message+=str(val)+"\tlen:"+str(len(vals[val]))+ str("min:" + "%.3f" % min(vals[val])) \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 + str("max:" + "%.3f" % max(vals[val])) + str("ave:" + "%.3f" % np.average(vals[val])) \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 + str("median:" + "%.3f" % np.sort(vals[val], axis=0)[len(vals[val])//2]) \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 + str("first:" + "%.3f" % vals[val][0]) + str("last:" + "%.3f" % vals[val][-1]) \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 + str("middle (no formatting):" + str(vals[val][len(vals[val])//2]) + "\n")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    message+="================================================================================\n"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef dequeue_all(sess, dequeue_op, logger, op_name=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    logger.debug(str(op_name) + ":starting to deque all examples")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            sess.run(dequeue_op, options=tf.RunOptions(timeout_in_ms=500))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            logger.debug(".")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except tf.errors.DeadlineExceededError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        logger.debug(str(op_name) + ":queue empty")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass QueueRunner(object):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  I borrowed this from a standard TensorFlow collection123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  The only difference between tf.QueueRunner and this one is that it does not close the queue after terminating123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  all threads. So I can initiate and kill threads on the same queue many times.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  Holds a list of enqueue operations for a queue, each to be run in a thread.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  Queues are a convenient TensorFlow mechanism to compute tensors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  asynchronously using multiple threads. For example in the canonical 'Input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  Reader' setup one set of threads generates filenames in a queue; a second set123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  of threads read records from the files, processes them, and enqueues tensors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  on a second queue; a third set of threads dequeues these input records to123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  construct batches and runs them through training operations.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  There are several delicate issues when running multiple threads that way:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  closing the queues in sequence as the input is exhausted, correctly catching123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  and reporting exceptions, etc.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  The `QueueRunner`, combined with the `Coordinator`, helps handle these issues.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def __init__(self, queue=None, enqueue_ops=None, close_op=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF               cancel_op=None, queue_closed_exception_types=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF               queue_runner_def=None, import_scope=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Create a QueueRunner.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    On construction the `QueueRunner` adds an op to close the queue.  That op123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    will be run if the enqueue ops raise exceptions.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    When you later call the `create_threads()` method, the `QueueRunner` will123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    create one thread for each op in `enqueue_ops`.  Each thread will run its123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    enqueue op in parallel with the other threads.  The enqueue ops do not have123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    to all be the same op, but it is expected that they all enqueue tensors in123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    `queue`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue: A `Queue`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      enqueue_ops: List of enqueue ops to run in threads later.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      close_op: Op to close the queue. Pending enqueue ops are preserved.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      cancel_op: Op to close the queue and cancel pending enqueue ops.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_closed_exception_types: Optional tuple of Exception types that123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        indicate that the queue has been closed when raised during an enqueue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        operation.  Defaults to `(tf.errors.OutOfRangeError,)`.  Another common123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        case includes `(tf.errors.OutOfRangeError, tf.errors.CancelledError)`,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        when some of the enqueue ops may dequeue from other Queues.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_runner_def: Optional `QueueRunnerDef` protocol buffer. If specified,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        recreates the QueueRunner from its contents. `queue_runner_def` and the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        other arguments are mutually exclusive.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      import_scope: Optional `string`. Name scope to add. Only used when123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        initializing from protocol buffer.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Raises:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      ValueError: If both `queue_runner_def` and `queue` are both specified.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      ValueError: If `queue` or `enqueue_ops` are not provided when not123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        restoring from `queue_runner_def`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if queue_runner_def:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      if queue or enqueue_ops:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise ValueError("queue_runner_def and queue are mutually exclusive.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._init_from_proto(queue_runner_def,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            import_scope=import_scope)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._init_from_args(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          queue=queue, enqueue_ops=enqueue_ops,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          close_op=close_op, cancel_op=cancel_op,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          queue_closed_exception_types=queue_closed_exception_types)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Protect the count of runs to wait for.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._lock = threading.Lock()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # A map from a session object to the number of outstanding queue runner123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # threads for that session.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._runs_per_session = weakref.WeakKeyDictionary()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # List of exceptions raised by the running threads.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._exceptions_raised = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def _init_from_args(self, queue=None, enqueue_ops=None, close_op=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                      cancel_op=None, queue_closed_exception_types=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Create a QueueRunner from arguments.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue: A `Queue`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      enqueue_ops: List of enqueue ops to run in threads later.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      close_op: Op to close the queue. Pending enqueue ops are preserved.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      cancel_op: Op to close the queue and cancel pending enqueue ops.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_closed_exception_types: Tuple of exception types, which indicate123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        the queue has been safely closed.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Raises:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      ValueError: If `queue` or `enqueue_ops` are not provided when not123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        restoring from `queue_runner_def`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      TypeError: If `queue_closed_exception_types` is provided, but is not123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        a non-empty tuple of error types (subclasses of `tf.errors.OpError`).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not queue or not enqueue_ops:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      raise ValueError("Must provide queue and enqueue_ops.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._queue = queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._enqueue_ops = enqueue_ops123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._close_op = close_op123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._cancel_op = cancel_op123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if queue_closed_exception_types is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      if (not isinstance(queue_closed_exception_types, tuple)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          or not queue_closed_exception_types123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          or not all(issubclass(t, errors.OpError)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                     for t in queue_closed_exception_types)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise TypeError(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            "queue_closed_exception_types, when provided, "123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            "must be a non-empty list of tf.error types, but saw: %s"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            % queue_closed_exception_types)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._queue_closed_exception_types = queue_closed_exception_types123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Close when no more will be produced, but pending enqueues should be123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # preserved.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if self._close_op is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._close_op = self._queue.close()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Close and cancel pending enqueues since there was an error and we want123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # to unblock everything so we can cleanly exit.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if self._cancel_op is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._cancel_op = self._queue.close(cancel_pending_enqueues=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not self._queue_closed_exception_types:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._queue_closed_exception_types = (errors.OutOfRangeError,)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._queue_closed_exception_types = tuple(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          self._queue_closed_exception_types)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def _init_from_proto(self, queue_runner_def, import_scope=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Create a QueueRunner from `QueueRunnerDef`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_runner_def: Optional `QueueRunnerDef` protocol buffer.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      import_scope: Optional `string`. Name scope to add.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    assert isinstance(queue_runner_def, queue_runner_pb2.QueueRunnerDef)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    g = ops.get_default_graph()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._queue = g.as_graph_element(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ops.prepend_name_scope(queue_runner_def.queue_name, import_scope))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._enqueue_ops = [g.as_graph_element(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ops.prepend_name_scope(op, import_scope))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         for op in queue_runner_def.enqueue_op_name]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._close_op = g.as_graph_element(ops.prepend_name_scope(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        queue_runner_def.close_op_name, import_scope))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._cancel_op = g.as_graph_element(ops.prepend_name_scope(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        queue_runner_def.cancel_op_name, import_scope))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    self._queue_closed_exception_types = tuple(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        errors.exception_type_from_error_code(code)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for code in queue_runner_def.queue_closed_exception_types)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Legacy support for old QueueRunnerDefs created before this field123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # was added.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not self._queue_closed_exception_types:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._queue_closed_exception_types = (errors.OutOfRangeError,)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  @property123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def queue(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return self._queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  @property123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def enqueue_ops(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return self._enqueue_ops123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  @property123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def close_op(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return self._close_op123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  @property123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def cancel_op(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return self._cancel_op123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  @property123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def queue_closed_exception_types(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return self._queue_closed_exception_types123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  @property123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def exceptions_raised(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Exceptions raised but not handled by the `QueueRunner` threads.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Exceptions raised in queue runner threads are handled in one of two ways123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    depending on whether or not a `Coordinator` was passed to123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    `create_threads()`:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    * With a `Coordinator`, exceptions are reported to the coordinator and123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      forgotten by the `QueueRunner`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    * Without a `Coordinator`, exceptions are captured by the `QueueRunner` and123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      made available in this `exceptions_raised` property.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      A list of Python `Exception` objects.  The list is empty if no exception123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      was captured.  (No exceptions are captured when using a Coordinator.)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return self._exceptions_raised123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  @property123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def name(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """The string name of the underlying Queue."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return self._queue.name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  # pylint: disable=broad-except123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def _run(self, sess, enqueue_op, coord=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Execute the enqueue op in a loop, close the queue in case of error.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      sess: A Session.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      enqueue_op: The Operation to run.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      coord: Optional Coordinator object for reporting errors and checking123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for stop conditions.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    decremented = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if coord and coord.should_stop():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          break123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          sess.run(enqueue_op)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        except self._queue_closed_exception_types:  # pylint: disable=catching-non-exception123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          # This exception indicates that a queue was closed.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          with self._lock:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self._runs_per_session[sess] -= 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            decremented = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if self._runs_per_session[sess] == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF              try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                sess.run(self._close_op)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF              except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                # Intentionally ignore errors from close_op.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                logging.vlog(1, "Ignored exception: %s", str(e))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      # This catches all other exceptions.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      if coord:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coord.request_stop(e)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        logging.error("Exception in QueueRunner: %s", str(e))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        with self._lock:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          self._exceptions_raised.append(e)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    finally:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      # Make sure we account for all terminations: normal or errors.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      if not decremented:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        with self._lock:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          self._runs_per_session[sess] -= 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def _close_on_stop(self, sess, cancel_op, coord):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Close the queue when the Coordinator requests stop.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      sess: A Session.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      cancel_op: The Operation to run.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      coord: Coordinator.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord.wait_for_stop()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # TODO(maksym): the next two lines are the only difference from TF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sess.run(cancel_op)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      # Intentionally ignore errors from cancel_op.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      logging.vlog(1, "Ignored exception: %s", str(e))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  # pylint: enable=broad-except123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def create_threads(self, sess, logger, coord=None, daemon=False, start=False):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Create threads to run the enqueue ops for the given session.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    This method requires a session in which the graph was launched.  It creates123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    a list of threads, optionally starting them.  There is one thread for each123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    op passed in `enqueue_ops`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    The `coord` argument is an optional coordinator that the threads will use123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    to terminate together and report exceptions.  If a coordinator is given,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    this method starts an additional thread to close the queue when the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coordinator requests a stop.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    If previously created threads for the given session are still running, no123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    new threads will be created.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      sess: A `Session`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      coord: Optional `Coordinator` object for reporting errors and checking123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stop conditions.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      daemon: Boolean.  If `True` make the threads daemon threads.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      start: Boolean.  If `True` starts the threads.  If `False` the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        caller must call the `start()` method of the returned threads.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      A list of threads.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with self._lock:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if self._runs_per_session[sess] > 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          # Already started: no new threads to return.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          return []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      except KeyError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # We haven't seen this session yet.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._runs_per_session[sess] = len(self._enqueue_ops)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      self._exceptions_raised = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ret_threads = [threading.Thread(target=self._run, args=(sess, op, coord))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                   for op in self._enqueue_ops]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if coord:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      ret_threads.append(threading.Thread(target=self._close_on_stop,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                          args=(sess, self._cancel_op, coord)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    started_threads = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for t in ret_threads:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      if coord:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coord.register_thread(t)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      if daemon:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        t.daemon = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      if start:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        log_message = ""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        t.start()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        log_message += str("[tr:" + str(started_threads) + "]")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        logger.debug(log_message)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        started_threads+=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return ret_threads123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def to_proto(self, export_scope=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Converts this `QueueRunner` to a `QueueRunnerDef` protocol buffer.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      export_scope: Optional `string`. Name scope to remove.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      A `QueueRunnerDef` protocol buffer, or `None` if the `Variable` is not in123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      the specified name scope.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if (export_scope is None or123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.queue.name.startswith(export_scope)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_runner_def = queue_runner_pb2.QueueRunnerDef()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_runner_def.queue_name = ops.strip_name_scope(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          self.queue.name, export_scope)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      for enqueue_op in self.enqueue_ops:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        queue_runner_def.enqueue_op_name.append(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ops.strip_name_scope(enqueue_op.name, export_scope))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_runner_def.close_op_name = ops.strip_name_scope(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          self.close_op.name, export_scope)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_runner_def.cancel_op_name = ops.strip_name_scope(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          self.cancel_op.name, export_scope)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      queue_runner_def.queue_closed_exception_types.extend([123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          errors.error_code_from_exception_type(cls)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          for cls in self._queue_closed_exception_types])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      return queue_runner_def123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      return None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  @staticmethod123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  def from_proto(queue_runner_def, import_scope=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Returns a `QueueRunner` object created from `queue_runner_def`."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return QueueRunner(queue_runner_def=queue_runner_def,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       import_scope=import_scope)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef int_repeat(integers,repeats):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Repeats every integer number of repeats time.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        integers: tensor of shape [1], tf.int32/tf.int64123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        repeats: tensor of shape [1], tf.int32/tf.int32 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns: 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tensor of shape [1] of the length sum(repeats)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    integers = tf.to_int_32(integers)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    repeats = tf.to_int32(repeats)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: assert shape is equal123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    max_repeats = tf.reduce_max(repeats)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    template = tf.tile(tf.expand_dims(integers,1),[1,max_repeats])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    mask = tf.sequence_mask(repeats,max_repeats)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    int_repeat = tf.boolean_mask(template,mask)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return int_repeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef int_sequence(starts,lengths):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Generates multiple sequences of integers. A generalized version of np.arange() for many sequences of integers instead of one.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        starts: start of the integer sequence; tensor of shape [1], tf.int32/tf.int64123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        length: length of the integer sequence; tensor of shape [1], tf.int32/tf.int32 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tensor of shape [1] of the length sum(repeats)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    starts = tf.to_int32(starts)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    repeats = tf.to_int32(repeats)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: assert shape is equal123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    max_length = tf.reduce_max(lengths)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_sequences = tf.shape(starts)[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    template = tf.tile(tf.expand_dims(tf.range(max_length),0),[num_sequences,1]) + tf.expand_dims(starts,1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    mask = tf.sequence_mask(lengths,max_length)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    int_sequence = tf.boolean_mask(template,mask)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return int_sequence123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF