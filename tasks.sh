set -e

for command in "$@"
do
    case "${command}" in
        unit-test)
            poetry run pytest tests/
        ;;
        run-email)
            poetry run python -m email_reader.main
        ;;
	run)
	    poetry run python -m parser.main
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
