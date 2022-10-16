set -e

for command in "$@"
do
    case "${command}" in
        unit-test)
            poetry run pytest tests/
        ;;
	unit-test-converter)
	    poetry run pytest tests/test_converter.py
        ;;
	run)
	    poetry run python -m parser.main
	;;
	run-file)
	    poetry run python -m parser.main --email $CB_EMAIL_ADDRESS >> $CB_BEANCOUNT_LEDGER_DIR
	;;
	list-email-headers)
	    poetry run python -m parser.main -lh
	;;
        dev-setup)
            poetry install
        ;;
        *)
            echo "Invalid command: '${command}'"
            exit 1
        ;;
    esac
done
