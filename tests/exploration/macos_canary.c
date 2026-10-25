/* Synthetic OS canary: no Python, producer imports, audit hook or external host. */
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 3) return 64;
    char *end = NULL;
    long port = strtol(argv[2], &end, 10);
    if (!end || *end || port < 1 || port > 65535) return 64;
    const char marker[] = "m3-canary\n";
    int write_error = 0, network_error = 0;
    int fd = open(argv[1], O_WRONLY | O_TRUNC | O_NOFOLLOW);
    if (fd < 0) {
        write_error = errno;
    } else {
        ssize_t count = write(fd, marker, sizeof(marker) - 1);
        if (count != (ssize_t)(sizeof(marker) - 1))
            write_error = count < 0 ? errno : EIO;
        if (close(fd) < 0 && !write_error) write_error = errno;
    }
    int connection = socket(AF_INET, SOCK_STREAM, 0);
    if (connection < 0) {
        network_error = errno;
    } else {
        struct sockaddr_in address = {0};
        address.sin_family = AF_INET;
        address.sin_port = htons((unsigned short)port);
        address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
        if (connect(connection, (struct sockaddr *)&address, sizeof(address)) < 0)
            network_error = errno;
        if (close(connection) < 0 && !network_error) network_error = errno;
    }
    printf("{\"write_succeeded\":%s,\"network_succeeded\":%s,"
           "\"write_errno\":%d,\"network_errno\":%d}\n",
           write_error ? "false" : "true", network_error ? "false" : "true",
           write_error, network_error);
    return 0;
}
