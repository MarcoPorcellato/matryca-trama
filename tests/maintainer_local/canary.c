/* Synthetic native controls; no Python, producer import or audit hook. */
#define _DARWIN_C_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

static int file_control(const char *operation, const char *path) {
    int writing = strcmp(operation, "write") == 0;
    int descriptor = open(path, (writing ? O_WRONLY | O_TRUNC : O_RDONLY) | O_NOFOLLOW);
    if (descriptor < 0) return errno;
    int error = 0;
    if (writing) {
        const char marker[] = "ma-canary\n";
        ssize_t count = write(descriptor, marker, sizeof(marker) - 1);
        if (count != (ssize_t)(sizeof(marker) - 1)) error = count < 0 ? errno : EIO;
    } else {
        char marker = 0;
        ssize_t count = read(descriptor, &marker, 1);
        if (count != 1 || marker != 'm') error = count < 0 ? errno : EIO;
    }
    if (close(descriptor) < 0 && !error) error = errno;
    return error;
}

static int network_control(const char *operation, const char *target) {
    int unix_socket = strcmp(operation, "unix") == 0;
    int ipv6 = strcmp(operation, "tcp6") == 0;
    int datagram = strcmp(operation, "udp") == 0;
    int family = unix_socket ? AF_UNIX : (ipv6 ? AF_INET6 : AF_INET);
    unsigned short port = 0;
    if (!unix_socket) {
        char *end = NULL;
        errno = 0;
        long parsed = strtol(target, &end, 10);
        if (errno || !end || *end || parsed < 1 || parsed > 65535) return EINVAL;
        port = (unsigned short)parsed;
    }
    int descriptor = socket(family, datagram ? SOCK_DGRAM : SOCK_STREAM, 0);
    if (descriptor < 0) return errno;
    int error = 0;
    if (unix_socket) {
        struct sockaddr_un address = {0};
        address.sun_family = AF_UNIX;
        if (strlen(target) >= sizeof(address.sun_path)) {
            error = ENAMETOOLONG;
        } else {
            memcpy(address.sun_path, target, strlen(target) + 1);
            if (connect(descriptor, (struct sockaddr *)&address, sizeof(address)) < 0)
                error = errno;
        }
    } else if (ipv6) {
        struct sockaddr_in6 address = {0};
        address.sin6_family = AF_INET6;
        address.sin6_port = htons(port);
        address.sin6_addr = in6addr_loopback;
        if (connect(descriptor, (struct sockaddr *)&address, sizeof(address)) < 0)
            error = errno;
    } else {
        struct sockaddr_in address = {0};
        address.sin_family = AF_INET;
        address.sin_port = htons(port);
        address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
        if (datagram) {
            const char packet[] = "ma-datagram";
            ssize_t count = sendto(descriptor, packet, sizeof(packet) - 1, 0,
                                   (struct sockaddr *)&address, sizeof(address));
            if (count != (ssize_t)(sizeof(packet) - 1)) error = count < 0 ? errno : EIO;
        } else if (connect(descriptor, (struct sockaddr *)&address, sizeof(address)) < 0) {
            error = errno;
        }
    }
    if (close(descriptor) < 0 && !error) error = errno;
    return error;
}

int main(int argc, char **argv) {
    if (argc < 2) return 64;
    alarm(8);
    int error = 0, resolver_error = 0;
    if (strcmp(argv[1], "dns") == 0 && argc == 2) {
        struct addrinfo hints = {0}, *result = NULL;
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;
        errno = 0;
        resolver_error = getaddrinfo("example.com", NULL, &hints, &result);
        if (resolver_error) error = errno;
        if (!resolver_error && result == NULL) resolver_error = EAI_NONAME;
        if (result != NULL) freeaddrinfo(result);
    } else if (argc == 3 &&
               (strcmp(argv[1], "read") == 0 || strcmp(argv[1], "write") == 0)) {
        error = file_control(argv[1], argv[2]);
    } else if (argc == 3 &&
               (strcmp(argv[1], "tcp4") == 0 || strcmp(argv[1], "tcp6") == 0 ||
                strcmp(argv[1], "udp") == 0 || strcmp(argv[1], "unix") == 0)) {
        error = network_control(argv[1], argv[2]);
    } else {
        return 64;
    }
    printf("{\"succeeded\":%s,\"error\":%d,\"resolver_error\":%d}\n",
           error || resolver_error ? "false" : "true", error, resolver_error);
    return 0;
}
