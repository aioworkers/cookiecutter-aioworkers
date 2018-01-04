def test_worker_example(service_builder, wait_for_message):
    with service_builder(config={'worker_example': 'y'}) as service:
        wait_for_message(service, 'aioworkers.worker.base:OK')
