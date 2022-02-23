set -e

for command in "$@"
do
    case "${command}" in
        unit-test)
            poetry run pytest tests/
        ;;
	unit-test-parser)
	    poetry run pytest tests/test_parser.py
        ;;
	run-email)
            poetry run python -m email_reader.main
        ;;
	run)
	    poetry run python -m parser.main
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
